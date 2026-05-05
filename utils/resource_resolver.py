# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import quote, unquote

class MdxResourceResolver:
    """统一资源解析器：处理URL重写、安全检查、路由"""
    
    @staticmethod
    def check_path_safety(dict_id, path):
        """防止路径穿越 (如 ../../etc/passwd)"""
        if not path or '..' in path:
            return False
        # 规范化路径，防止反向斜杠等绕过
        safe_path = path.lstrip('/\\').replace('\\', '/')
        abs_dict_dir = os.path.dirname(os.path.abspath(dict_id))
        abs_resource = os.path.normpath(os.path.join(abs_dict_dir, safe_path))
        # 必须确保解析后的路径还在词典目录下
        return abs_resource.startswith(abs_dict_dir)

    @staticmethod
    def rewrite_html_resources(raw_html, dict_id, base_url):
        """从 window_api 抽离出来的 HTML 重写逻辑"""
        encoded_id = quote(unquote(dict_id), safe='')
        
        def replace_resource(match):
            attr_start, path, attr_end = match.group(1), match.group(2), match.group(3)
            if path.startswith(('http://', 'https://', 'data:', 'javascript:', '#')):
                return match.group(0)
            safe_path = quote(unquote(path), safe='')
            return f'{attr_start}{base_url}/resource?dict_id={encoded_id}&path={safe_path}{attr_end}'

        resource_pattern = re.compile(r'((?:src|href)\s*=\s*["\'])([^"\']+)(["\'])', re.IGNORECASE)
        
        # 剥离原有标签防止XSS/重复加载
        body_content = re.sub(r'<\?xml[^>]*\?>', '', raw_html)
        links = re.findall(r'<link\s+[^>]*?>', body_content, re.IGNORECASE)
        scripts = re.findall(r'<script[^>]*>[\s\S]*?</script>', body_content, re.IGNORECASE)
        for tag in links + scripts:
            body_content = body_content.replace(tag, '', 1)

        # 统一替换
        body_content = resource_pattern.sub(replace_resource, body_content)
        head_content = "\n".join([resource_pattern.sub(replace_resource, l) for l in links]) + \
                       "\n" + \
                       "\n".join([resource_pattern.sub(replace_resource, s) for s in scripts])
        return head_content, body_content

    @staticmethod
    def resolve_resource(dict_manager, dict_id, path):
        """供 ResourceServer 调用的统一入口"""
        path = unquote(path)
        dict_id = unquote(dict_id)
        
        if not MdxResourceResolver.check_path_safety(dict_id, path):
            return None # 拦截恶意请求
            
        return dict_manager.get_resource(dict_id, path)
