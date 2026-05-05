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
        self._entry_cache: Dict[str, str] = {}

    def load(self, variant_handler=None) -> bool:
        try:
            # 直接实例化，底层会自动判断使用缓存还是首次构建
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
        if not self.mdd: return None
        # 直接丢给 MDD 的归一化字典处理，O(1) 查找
        return self.mdd.get(path)

    def search(self, keyword: str, use_variants: bool) -> list:
        if not self.loaded or not keyword: return []
        results = []
        seen = set()
        
        # 直接调用底层块级二分搜索
        for key, idx in self.mdx.search_prefix(keyword, max_results=50):
            if key not in seen:
                seen.add(key)
                results.append((key, idx))
                
        if use_variants and self.variant_handler and self.variant_handler.should_expand(keyword):
            for v_kw in self.variant_handler.expand_keyword(keyword):
                for key, idx in self.mdx.search_prefix(v_kw, max_results=50):
                    if key not in seen:
                        seen.add(key)
                        results.append((key, idx))
        return results

    def get_content(self, key: str) -> str:
        if key in self._entry_cache: return self._entry_cache[key]
        
        # 通过 search 找到 idx，再走 LRU 高效获取
        search_res = self.mdx.search_prefix(key, max_results=1)
        if not search_res: return ""
        
        # 精确匹配判断
        matched_key, idx = search_res[0]
        if matched_key != key: return ""

        c = self.mdx.get_by_index(idx)
        if not c: return ""
        
        # 处理跳转链接
        c_stripped = c.strip() if isinstance(c, str) else c.decode('utf-8', errors='ignore').strip()
        if c_stripped.startswith("@@@LINK="):
            target_word = c_stripped.replace("@@@LINK=", "").strip()
            if target_word:
                target_html = self.get_content(target_word) # 递归走缓存
                return target_html if target_html else f'<div style="padding:8px;color:#888;">🔗 参见词条：<b>{target_word}</b></div>'
        
        self._entry_cache[key] = c_stripped
        return c_stripped

    def close(self):
        if self.mdx: self.mdx.close()
        if self.mdd: self.mdd.close()
