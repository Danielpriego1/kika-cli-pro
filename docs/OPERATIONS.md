# Operación y recuperación

Kika se ejecuta como `kika-orchestrator.service`. El servicio usa `Restart=always` y se inicia después de Engram. Su configuración desplegable se conserva en `deploy/systemd/`.

```zsh
sudo systemctl status kika-orchestrator.service
sudo journalctl -u kika-orchestrator.service -n 100 --no-pager
sudo systemctl restart kika-orchestrator.service
python3 scripts/verify_kika.py
```

La verificación debe confirmar: API saludable, 22 perfiles disponibles, persistencia y búsqueda en Engram, y creación de una delegación de QA.
