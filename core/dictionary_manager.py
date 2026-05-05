# -*- coding: utf-8 -*-
from core.mdx_wrapper import MdxWrapper
import os

class DictionaryManager:
    def __init__(self):
        self.loaded_dicts: dict[str, MdxWrapper] = {}  # 绝对路径 -> 实例
        self._variant_handler = None
        # 修复点1：程序启动时直接初始化异体字
        self._init_variant_handler()

    def _init_variant_handler(self):
        try:
            from libs.variants import VARIANTS
            from libs.variant_utils import VariantHandler
            print("首次加载异体字映射表...")
            self._variant_handler = VariantHandler(VARIANTS)
        except Exception as e:
            print(f"加载异体字失败: {e}")

    def load_mdx(self, path: str) -> bool:
        abs_path = os.path.abspath(path)
        if abs_path in self.loaded_dicts or not os.path.exists(abs_path):
            return abs_path in self.loaded_dicts
            
        wrapper = MdxWrapper(abs_path)
        # 直接传入已经初始化好的单例
        if wrapper.load(variant_handler=self._variant_handler):
            self.loaded_dicts[abs_path] = wrapper
            return True
        return False

    def unload_mdx(self, path: str):
        abs_path = os.path.abspath(path)
        if abs_path in self.loaded_dicts:
            self.loaded_dicts[abs_path].close()
            del self.loaded_dicts[abs_path]

    def search(self, keyword: str, use_variants: bool) -> list:
        if not self.loaded_dicts or not keyword: return []
        merged_results = {}
        for path, wrapper in self.loaded_dicts.items():
            for key, idx in wrapper.search(keyword, use_variants):
                if key not in merged_results:
                    merged_results[key] = {"key": key, "sources": []}
                if not any(s["dict_id"] == path for s in merged_results[key]["sources"]):
                    merged_results[key]["sources"].append({
                        "dict_id": path,
                        "dict_name": wrapper.name
                    })
        results = list(merged_results.values())
        results.sort(key=lambda x: len(x["key"]))
        return results

    def get_content(self, dict_id: str, key: str) -> tuple:
        abs_path = os.path.abspath(dict_id)
        wrapper = self.loaded_dicts.get(abs_path)
        if not wrapper: return "", ""
        return wrapper.get_content(key), wrapper.name

    def get_resource(self, dict_id: str, path: str) -> bytes:
        abs_path = os.path.abspath(dict_id)
        if abs_path not in self.loaded_dicts: return None
        wrapper = self.loaded_dicts[abs_path]
        data = None
        if wrapper.mdd:
            try: data = wrapper.mdd.get(path)
            except: pass
        if not data and wrapper.folder_path:
            try:
                file_path = os.path.join(wrapper.folder_path, path)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as f: data = f.read()
            except: pass
        if data:
            if isinstance(data, str):
                try: return data.encode('utf-8')
                except: return data.encode('gbk', errors='ignore')
            return data
        return None
