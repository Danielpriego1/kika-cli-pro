# Kika-AI: Operación del Núcleo

## Estado operativo

Kika-AI se ejecuta como el servicio `kika-orchestrator.service` en el VPS `85.239.241.120`. El servicio está habilitado al arranque, reinicia automáticamente ante una caída y escucha únicamente en `127.0.0.1:7488`. Esta restricción evita exponer su API de orquestación a Internet.

La memoria semántica se guarda en Engram bajo el proyecto explícito `kika-cli-pro`. El servicio no acepta comandos arbitrarios a través de la API: las delegaciones se convierten en archivos JSON auditables dentro de `runtime/queue/` y los perfiles que implican acciones sensibles quedan marcados para aprobación.

## 22 perfiles especializados

El registro se encuentra en `config/agent_registry.json`. Los perfiles son especializaciones de Kika, no 22 modelos independientes. Comparten tres runtimes locales verificados:

| Runtime | Uso dentro de Kika |
|---|---|
| `opencode` | Implementación, operaciones, integración, QA y documentación. |
| `pi` | Análisis, revisión, investigación y UX. |
| `gga` | Planificación y descomposición de objetivos. |
| `engram` | Memoria semántica persistente y trazabilidad. |

Los perfiles cubren coordinación, razonamiento, planificación, construcción, memoria, SRE, seguridad, QA, repositorios, arquitectura web, backend, frontend, móvil, datos, DevOps, investigación, documentación, producto, integraciones, automatización, UX e incidentes.

## Endpoints locales

| Ruta | Método | Función |
|---|---|---|
| `/health` | `GET` | Devuelve salud de Engram, los 22 perfiles y la cola. |
| `/agents` | `GET` | Devuelve los 22 perfiles y disponibilidad de sus runtimes. |
| `/status` | `GET` | Alias operativo de salud. |
| `/memory` | `POST` | Guarda una memoria verificada en Engram. |
| `/memory/search` | `POST` | Busca memoria en el proyecto `kika-cli-pro`. |
| `/dispatch` | `POST` | Registra una delegación estructurada en la cola. |

La API está ligada a loopback. Para acceder desde fuera se debe usar SSH, una aplicación privada autenticada o un proxy deliberadamente configurado; no se debe publicar el puerto 7488 directamente.

## Comandos de operación

```zsh
# Revisar el estado del servicio
sudo systemctl status kika-orchestrator.service

# Consultar registros recientes
sudo journalctl -u kika-orchestrator.service -n 100 --no-pager

# Ver la salud por API local
curl http://127.0.0.1:7488/health

# Reiniciar tras un cambio controlado
sudo systemctl restart kika-orchestrator.service

# Comprobar la memoria dedicada de Kika
engram stats
engram projects list
```

## Recuperación

El archivo de unidad de systemd incluye `Restart=always`. Si el proceso termina, systemd crea uno nuevo después de cinco segundos. Las pruebas de puesta en marcha verificaron que el PID cambia y que la API vuelve a responder tras una terminación controlada.

## Canal hacia iPhone

La salida de iMessage no forma parte del proceso de orquestación aún. El puente Mac/iPhone depende de que el túnel reverso `sshauto` esté activo y de que el Atajo `Kika Message` exista en la Mac. Cuando se habilite el túnel, el módulo `core/mac_notifier.py` debe integrarse explícitamente en eventos de tarea completada, incidente crítico y solicitud de aprobación.
