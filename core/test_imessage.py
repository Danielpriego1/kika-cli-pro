import requests
import sys

def test_imessage(title, message):
    url = 'http://localhost:9999'
    payload = {'title': title, 'message': message}
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            print('✅ Señal enviada al Mac con éxito.')
        else:
            print(f'❌ Error en el puente: {r.status_code}')
    except Exception as e:
        print(f'❌ No se pudo contactar con el Mac: {e}')

if __name__ == '__main__':
    title = sys.argv[1] if len(sys.argv) > 1 else 'Prueba de Sistema'
    message = sys.argv[2] if len(sys.argv) > 2 else 'Confirmando enlace de iMessage.'
    test_imessage(title, message)
