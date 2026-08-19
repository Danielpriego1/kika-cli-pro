# Kika-AI

Kika-AI es la orquestadora privada del ecosistema Grupo PSI. Este repositorio contiene el núcleo persistente, el registro de sus 22 perfiles especializados, las plantillas de runtime, las pruebas operativas, la integración Mac/iPhone y los recursos necesarios para desplegarla de forma reproducible en el VPS.

## Principios operativos

Kika trabaja con memoria semántica persistente mediante Engram, registra tareas antes de ejecutarlas y no acepta comandos arbitrarios por su API local. Las operaciones destructivas, publicaciones externas, cambios de credenciales y despliegues de producción requieren aprobación explícita conforme al perfil asignado.

## Estructura

| Ruta | Propósito |
|---|---|
| `core/` | Orquestador, memoria y módulos de notificación. |
| `config/agent_registry.json` | Registro declarativo de los 22 perfiles especializados. |
| `config/templates/` | Plantillas no secretas de Pi, MCP y skills. |
| `skills/installed/` | Copias de referencia de las skills instaladas para Kika. |
| `docs/` | Arquitectura, operación, agentes y dependencias. |
| `deploy/systemd/` | Unidad y variables de entorno para el servicio persistente. |
| `integrations/mac/` | Puente seguro hacia Atajos/macOS/iPhone. |
| `scripts/` | Verificación e instalación operativa. |
| `runtime/` | Estado local, cola y resultados; ignorado por Git. |

## Servicio local

El proceso `kika-orchestrator.service` expone una API exclusivamente local en `127.0.0.1:7488`.

```zsh
curl http://127.0.0.1:7488/health
curl http://127.0.0.1:7488/agents
sudo systemctl status kika-orchestrator.service
```

Consulta `docs/OPERATIONS.md` para operación y recuperación, y `docs/AGENTS.md` para el mapa de los 22 perfiles.
