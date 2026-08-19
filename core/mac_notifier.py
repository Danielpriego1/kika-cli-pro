import os
import requests
import json

class MacTunnelNotifier:
    def __init__(self, tunnel_url=None):
        # El puerto del túnel reverso que apunta a tu Mac (ej. http://localhost:9999)
        self.tunnel_url = tunnel_url or os.getenv("MAC_TUNNEL_URL", "http://localhost:9999")

    def send_imessage(self, title, message):
        payload = {
            "title": title,
            "message": message
        }
        try:
            response = requests.post(self.tunnel_url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"[Error sending to Mac tunnel]: {e}")
            return False

if __name__ == '__main__':
    notifier = MacTunnelNotifier()
    print('Mac Tunnel Notifier initialized.')
