#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -f /etc/kika/kika.env ]]; then
  echo "Copia deploy/systemd/kika.env.example a /etc/kika/kika.env y ajusta las rutas antes de continuar." >&2
  exit 1
fi
sudo install -o root -g root -m 0644 "$ROOT/deploy/systemd/kika-orchestrator.service" /etc/systemd/system/kika-orchestrator.service
sudo systemctl daemon-reload
sudo systemctl enable --now kika-orchestrator.service
sudo systemctl status kika-orchestrator.service --no-pager
