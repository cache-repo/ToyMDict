# -*- coding: utf-8 -*-
import os
from typing import List, Dict, Optional
from libs.readmdict import CachedMDX, CachedMDD

class MdxWrapper:
    def __init__(self, mdx_path: str):
        self.mdx_path = mdx_path
        self.folder_path = os.path.dirname(mdx_path)
        self.path = mdx_path
        self.name = os.path.splitext(os.path.basename(mdx_path))[0]
        self.dict_id = os.path.abspath(mdx_path)
        self.mdx = None
        self.mdd = None
        self.loaded = False
        self.variant_handler = None
        self._entry_cache: Dict[tuple, str] = {}  # 修改：缓存键改为 (key, idx) 元组

    def load(self, variant_handler=None) -> bool:
        try:
            self.mdx = CachedMDX(self.path, encoding='utf-8')
            mdd_path = os.path.join(self.folder_path, self.name + '.mdd')
            if os.path.exists(mdd_path):
                self.mdd = CachedMDD(mdd_path, encoding='utf-8')
            self.variant_handler = variant_handler
            self.loaded = True
            return True
        except Exception as e:
            print(f"加载 {self.path} 失败: {e}")
            return False

    def get_resource(self, path: str) -> Optional[bytes]:
        if not self.mdd:
            return None
        return self.mdd.get(path)

    def search(self, keyword: str, use_variants: bool) -> list:
        if not self.loaded or not keyword:
            return []
        results = []
        seen_idx = set()  # 修改：使用 idx 去重，避免异体字搜索重复返回同一词条
        for key, idx in self.mdx.search_prefix(keyword, max_results=50):
            if idx not in seen_idx:
                seen_idx.add(idx)
                results.append((key, idx))
        if use_variants and self.variant_handler and self.variant_handler.should_expand(keyword):
            for v_kw in self.variant_handler.expand_keyword(keyword):
                for key, idx in self.mdx.search_prefix(v_kw, max_results=50):
                    if idx not in seen_idx:
                        seen_idx.add(idx)
                        results.append((key, idx))
        return results

    def get_content(self, key: str, idx: int = None) -> str:  # 修改：增加 idx 参数
        # 优先使用 idx 获取，解决同名词条只加载第一条的问题
        if idx is not None:
            if (key, idx) in self._entry_cache:
                return self._entry_cache[(key, idx)]
            c = self.mdx.get_by_index(idx)
            if not c:
                return ""
            c_stripped = c.strip() if isinstance(c, str) else c.decode('utf-8', errors='ignore').strip()
            if c_stripped.startswith("@@@LINK="):
                target_word = c_stripped.replace("@@@LINK=", "").strip()
                if target_word:
                    target_html = self.get_content(target_word)
                    return target_html if target_html else f'<div style="padding:8px;color:#888;">🔗 参见词条：<b>{target_word}</b></div>'
            self._entry_cache[(key, idx)] = c_stripped
            return c_stripped

        # 兼容旧调用：如果没有传 idx，退回只用 key 查询的逻辑
        if key in self._entry_cache:
            return self._entry_cache[key]
        search_res = self.mdx.search_prefix(key, max_results=1)
        if not search_res:
            return ""
        matched_key, idx = search_res[0]
        if matched_key != key:
            return ""
        return self.get_content(key, idx)
    
    def close(self):
        if self.mdx:
            self.mdx.close()
        if self.mdd:
            self.mdd.close()
