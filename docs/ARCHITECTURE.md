# Arquitectura de Kika-AI

```text
Usuario ── iPhone/iMessage ── Mac + Atajo ── túnel SSH reverso ── Kika-AI (VPS)
                                                                  │
                                                                  ├─ API local 127.0.0.1:7488
                                                                  ├─ registro de 22 perfiles
                                                                  ├─ cola auditable de delegaciones
                                                                  ├─ Engram: memoria semántica
                                                                  ├─ Pi: análisis y revisión
                                                                  ├─ GGA: planificación
                                                                  └─ OpenCode: implementación y operación
```

Kika es el único punto de coordinación. Los 22 perfiles son especializaciones con permisos y criterios de aprobación definidos en `config/agent_registry.json`. La API se mantiene en loopback para que no sea accesible desde Internet por defecto.
