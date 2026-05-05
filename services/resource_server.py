# -*- coding: utf-8 -*-
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from utils.resource_resolver import MdxResourceResolver
from utils.path_helper import get_mime_type

class ResourceHandler(BaseHTTPRequestHandler):
    dict_manager = None

    def log_message(self, format, *args): pass

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            if parsed.path == '/resource':
                query = parse_qs(parsed.query)
                dict_id = query.get('dict_id', [None])[0]
                path = query.get('path', [None])[0]
                
                if path and dict_id and self.dict_manager:
                    # 直接委托给 Resolver，不再自己处理编解码和业务逻辑
                    data = MdxResourceResolver.resolve_resource(self.dict_manager, dict_id, path)
                    if data:
                        mime_type = get_mime_type(path) # 沿用原来的mime逻辑
                        self.send_response(200)
                        self.send_header('Content-Type', mime_type)
                        self.send_header('Cache-Control', 'public, max-age=31536000')
                        self.send_header('Content-Length', str(len(data)))
                        self.end_headers()
                        self.wfile.write(data)
                        return
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            print(f"资源服务器错误: {e}")
            self.send_response(500)
            self.end_headers()


class ResourceServer:
    def __init__(self, dict_manager, port: int = 8765):
        self.dict_manager = dict_manager
        self.port = port
        self.server = None

    def start(self):
        import threading
        ResourceHandler.dict_manager = self.dict_manager
        for port in range(self.port, self.port + 50):
            try:
                self.server = ThreadingHTTPServer(('localhost', port), ResourceHandler)  # ← 改这里
                self.port = port
                break
            except OSError:
                continue
        if not self.server:
            raise RuntimeError("无法找到可用端口")
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def stop(self):
        if self.server:
            self.server.shutdown()

    def stop(self):
        if self.server: self.server.shutdown()
