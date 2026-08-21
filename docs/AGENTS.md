# Perfiles especializados de Kika-AI

La fuente de verdad es [`config/agent_registry.json`](../config/agent_registry.json). Los perfiles especializados no son modelos duplicados: Kika los enruta a los runtimes reales instalados —**OpenCode, Pi, GGA y Engram**— según su función, capacidades y política de aprobación.

## Registro extensible

El registro usa el esquema `1.1` y puede ampliarse sin modificar el número esperado dentro del núcleo. La política actual requiere un mínimo de **22 perfiles**, permite expansión y restringe los runtimes a los cuatro adaptadores ya validados. Un perfil nuevo solo se activa si declara un identificador único, runtime permitido, rol, capacidades y acciones que requieren aprobación.

| Área | Perfiles |
|---|---|
| Coordinación | Kika Coordinadora, Pi Razonadora y GGA Planificadora. |
| Construcción | OpenCode Constructora, Arquitecta Web, Ingeniería Backend, Frontend y Móvil. |
| Operación | SRE, DevOps, Datos, Automatización, Incidentes y Centinela VPS. |
| Control y seguridad | Auditora de Seguridad, Revisora de Exposición de Red, QA, Repositorios, UX, Documentación y Control de Cambios. |
| Inteligencia y continuidad | Engram Archivista, Curadora Engram, Investigación, Producto, Integraciones, Capacidad y Recuperación. |
| Productos y canales | Diseñadora de Aprendizaje, Analista QA Grupo PSI y Custodia del Canal iPhone. |
| Entrega | Gestora de Releases. |

## Perfiles añadidos

| Perfil | Runtime | Alcance inicial | Aprobación requerida |
|---|---|---|---|
| Centinela VPS | OpenCode | Salud, carga, disco, memoria y puertos. | No; solo lectura. |
| Revisora de Exposición de Red | Pi | Análisis de red y riesgo. | Cambio de firewall o exposición de puertos. |
| Gestora de Releases | OpenCode | Preparación de versión, pruebas y rollback. | Publicar en Git o desplegar. |
| Planificadora de Recuperación | Pi | Continuidad, dependencias y recuperación. | Restaurar respaldo o detener servicio. |
| Curadora Engram | Engram | Calidad, deduplicación y recuperación de memoria. | Borrar memoria. |
| Custodia del Canal iPhone | OpenCode | Diagnóstico de Atajos y SSH restringido. | Cambiar o rotar credenciales. |
| Diseñadora de Aprendizaje | Pi | Rutas y pistas del Polyglot Coding Game. | Publicación externa. |
| Analista QA Grupo PSI | OpenCode | Pruebas reproducibles de Grupo PSI. | No; solo pruebas. |
| Analista de Capacidad | OpenCode | Tendencias de recursos y contenedores. | No; solo lectura. |
| Coordinadora de Control de Cambios | GGA | Riesgo, dependencias y evidencia de cambios. | Despliegue, credenciales o borrado de datos. |

Cada delegación se conserva en `runtime/queue/` y guarda una huella de contexto en Engram. Las tareas sensibles quedan como `pending_approval`. Ningún perfil nuevo obtiene ejecución libre de terminal, publicación externa, cambios de credenciales, borrado de datos o despliegues sin un paso de aprobación explícito.
