# Los 22 perfiles de Kika

La fuente de verdad es `config/agent_registry.json`. Los perfiles no son 22 modelos duplicados: se enrutan a los runtimes locales Pi, GGA, OpenCode y Engram según su función.

| Área | Perfiles |
|---|---|
| Coordinación | Kika Coordinadora, Pi Razonadora, GGA Planificadora. |
| Construcción | OpenCode Constructora, Arquitecta Web, Backend, Frontend y Móvil. |
| Operación | SRE, DevOps, Datos, Automatización e Incidentes. |
| Control | Seguridad, QA, Repositorios, UX y Documentación. |
| Inteligencia | Engram Archivista, Investigación, Producto e Integraciones. |

Cada delegación queda en `runtime/queue/` y se almacena una huella de contexto en Engram. Las tareas sensibles se registran como `pending_approval`.
