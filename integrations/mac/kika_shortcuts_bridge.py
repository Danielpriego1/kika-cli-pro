#!/usr/bin/env python3
"""Receptor local para macOS; envía el texto recibido al Atajo 'Kika Message'.

Ejecutar únicamente en la Mac del propietario y publicar el puerto mediante un
SSH reverse tunnel. El Atajo conserva el destinatario de iMessage; este archivo
no contiene números ni credenciales.
"""
import http.server
import json
import subprocess

PORT = 9999
SHORTCUT = "Kika Message"

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        size = int(self.headers.get("Content-Length", "0"))
        if size <= 0 or size > 12000:
            self.send_response(400)
            self.end_headers()
            return
        payload = json.loads(self.rfile.read(size).decode("utf-8"))
        text = "[Kika-AI] {title}\n\n{message}".format(
            title=str(payload.get("title", "Alerta")),
            message=str(payload.get("message", "")),
        )
        completed = subprocess.run(["shortcuts", "run", SHORTCUT, "-i", text], check=False)
        self.send_response(200 if completed.returncode == 0 else 502)
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
