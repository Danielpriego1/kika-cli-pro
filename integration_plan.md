# Plan de Integración: El Enjambre de 22 Agentes de Kika 🛡️🤖🪖

Este documento detalla la estrategia para convertir a **Kika** en la Generalísima de un ejército de 22 agentes especializados del ecosistema **Gentle-AI**, integrados con la memoria semántica de **Engram**.

## 1. Categorización del Ejército (Los 22 Especialistas)
Hemos identificado y clasificado a los agentes en cuatro divisiones estratégicas para maximizar la eficiencia en el VPS:

| División | Agentes / Skills Clave | Responsabilidad |
| :--- | :--- | :--- |
| **Estrategia y Workflow** | `sdd-flow`, `branch-pr`, `issue-creation`, `backlog-triage` | Planificación de tareas, gestión de versiones y priorización de objetivos. |
| **Calidad y Blindaje** | `architecture-guardrails`, `testing-coverage`, `commit-hygiene`, `pr-review-deep` | Asegurar que el código sea perfecto, seguro y siga las normas del servidor. |
| **Desarrollo Especializado** | `server-api`, `ui-elements`, `dashboard-htmx`, `visual-language` | Creación de backend, interfaces TUI y mantenimiento de la identidad visual. |
| **Operaciones y Memoria** | `memory-protocol`, `plugin-thin`, `gentleman-bubbletea` | Gestión de la memoria en Engram y orquestación de scripts ligeros. |

## 2. Lógica de Orquestación: El Mando de Kika
Kika no realiza todas las tareas; ella las **orquesta** siguiendo este flujo de decisión:

1.  **Descomposición (SDD)**: Kika recibe una orden compleja y usa el agente `sdd-flow` para dividirla en sub-tareas atómicas.
2.  **Despacho (Dispatch)**: Kika selecciona al agente más apto para cada sub-tarea usando el binario de `gentle-ai`.
3.  **Supervisión (Review)**: Antes de dar por terminada una tarea, Kika invoca al agente `pr-review-deep` para validar que el trabajo cumpla con los estándares.
4.  **Feedback**: Si un agente falla, Kika analiza el log y reasigna la tarea con nuevas instrucciones.

## 3. Integración con Engram: Memoria Compartida
Para que el enjambre funcione como una sola unidad, Engram servirá como el **Contexto Unificado**:

-   **Memoria de Sesión**: Cada agente lee el estado actual del proyecto desde Engram antes de empezar.
-   **Consolidación de Conocimiento**: Al terminar, el agente guarda su "lección aprendida" en Engram.
-   **Sincronización**: Kika usa Engram para saber qué agente está haciendo qué, evitando conflictos de edición en el servidor.

## 4. Hoja de Ruta de Implementación (Roadmap)

### Fase 1: Preparación del Cuartel General (Hoy)
-   Configurar las variables de entorno en el VPS 2 (`85.239.241.120`).
-   Indexar el catálogo de 22 agentes en la base de datos vectorial de Engram.

### Fase 2: Entrenamiento de Orquestación
-   Pruebas de despacho: Kika enviando tareas simples a agentes de infraestructura.
-   Ajuste de prompts en OpenRouter para mejorar la delegación.

### Fase 3: Despliegue del Enjambre (Mañana)
-   Activación del monitoreo de "Auto-Sanación" para Grupo PSI.
-   Primera tarea compleja: "Auditar y optimizar la base de datos de InsForge".

---
**Estado del Proyecto**: 🛡️ **LISTO PARA INICIAR FASE 1**
**Orquestadora**: Kika CLI Pro
**Infraestructura**: VPS 2 (Contabo) + Engram + Gentle-AI
