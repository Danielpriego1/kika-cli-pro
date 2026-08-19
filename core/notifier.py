import os
import requests
import json

class KikaNotifier:
    def __init__(self, bark_key=None):
        self.bark_key = bark_key or os.getenv("BARK_KEY", "")
        self.base_url = f"https://api.day.app/{self.bark_key}"

    def send_alert(self, title, message, level='info'):
        if not self.bark_key:
            print("[Warning] BARK_KEY not set. Notification skipped.")
            return False
        
        url = f"{self.base_url}/{requests.utils.quote(title)}/{requests.utils.quote(message)}"
        payload = {
            "icon": "https://img.icons8.com/color/48/artificial-intelligence.png",
            "group": "Kika-AI",
            "level": level
        }
        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"[Error sending notification]: {e}")
            return False

if __name__ == '__main__':
    notifier = KikaNotifier()
    print('Notifier module initialized.')
