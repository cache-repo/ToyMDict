# -*- coding: utf-8 -*-
import os
from urllib.parse import quote, unquote

def safe_url_encode(path: str) -> str:
    """处理特殊字符图片路径，防止双重编码"""
    if not path: return ""
    # 防止原本就是 %xx 格式被二次编码，先解码一次还原
    decoded_path = unquote(path)
    return quote(decoded_path)

def get_mime_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    mime_map = {
        '.css': 'text/css', '.js': 'application/javascript',
        '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.gif': 'image/gif', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
        '.mp3': 'audio/mpeg', '.ogg': 'audio/ogg', '.wav': 'audio/wav', '.mp4': 'video/mp4',
    }
    return mime_map.get(ext, 'application/octet-stream')

def find_mdx_files(folder_path: str) -> list:
    """递归遍历文件夹获取所有 mdx 文件"""
    mdx_files = []
    if not os.path.exists(folder_path):
        return mdx_files
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith('.mdx'):
                mdx_files.append(os.path.join(root, f))
    return mdx_files
