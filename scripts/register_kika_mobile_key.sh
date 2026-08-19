#!/usr/bin/env bash
set -euo pipefail

PUBLIC_KEY_FILE="${1:-}"
USER_NAME="kika-mobile"
PROJECT_ENTRY="/home/dani/kika-cli-pro/integrations/iphone/kika_ssh_entry.py"
ENTRYPOINT="/usr/local/lib/kika/kika_ssh_entry.py"

if [[ -z "$PUBLIC_KEY_FILE" || ! -f "$PUBLIC_KEY_FILE" ]]; then
  echo "Uso: sudo $0 /ruta/a/clave-publica.pub" >&2
  exit 64
fi
if [[ ! -f "$PROJECT_ENTRY" ]]; then
  echo "No se encontró el receptor de Kika en $PROJECT_ENTRY." >&2
  exit 70
fi

install -d -o root -g root -m 0755 /usr/local/lib/kika
install -o root -g root -m 0755 "$PROJECT_ENTRY" "$ENTRYPOINT"

public_key="$(tr -d '\r\n' < "$PUBLIC_KEY_FILE")"
if [[ ! "$public_key" =~ ^ssh-(ed25519|rsa|ecdsa)[[:space:]] ]]; then
  echo "La clave pública no tiene un formato SSH admitido." >&2
  exit 64
fi

if ! id "$USER_NAME" >/dev/null 2>&1; then
  useradd --create-home --home-dir "/home/$USER_NAME" --shell /bin/sh "$USER_NAME"
else
  usermod --shell /bin/sh "$USER_NAME"
fi

install -d -o "$USER_NAME" -g "$USER_NAME" -m 0700 "/home/$USER_NAME/.ssh"
printf 'command="%s",no-port-forwarding,no-agent-forwarding,no-X11-forwarding,no-pty,no-user-rc %s\n' "$ENTRYPOINT" "$public_key" > "/home/$USER_NAME/.ssh/authorized_keys"
chown "$USER_NAME:$USER_NAME" "/home/$USER_NAME/.ssh/authorized_keys"
chmod 0600 "/home/$USER_NAME/.ssh/authorized_keys"

echo "Cuenta restringida $USER_NAME lista. La clave solo puede invocar el receptor de Kika."
