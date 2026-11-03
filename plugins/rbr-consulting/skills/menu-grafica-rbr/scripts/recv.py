import http.server,os,urllib.parse
D="~/Desktop/AI/RBR AI/consegne/2026-10-09/img/originali"
class H(http.server.BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin','https://chatgpt.com')
        self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','*')
        self.send_header('Access-Control-Allow-Private-Network','true')
    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        q=urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query); n=os.path.basename(q['name'][0])
        if not n.startswith('lb_') or not n.endswith('.png'): self.send_response(400); self.end_headers(); return
        data=self.rfile.read(int(self.headers['Content-Length']))
        open(os.path.join(D,n),'wb').write(data)
        self.send_response(200); self.cors(); self.end_headers(); self.wfile.write(b'ok %d'%len(data))
http.server.HTTPServer(('127.0.0.1',8765),H).serve_forever()

