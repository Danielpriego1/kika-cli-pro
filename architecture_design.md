# Arquitectura de Memoria Semántica: Kika + Engram 🧠🛡️

Esta arquitectura define cómo **Kika** utiliza **Engram** como su sistema de memoria persistente y semántica para operar como un brazo derecho técnico autónomo y preciso.

## 1. Componentes del Ecosistema

| Componente | Función | Ubicación |
| :--- | :--- | :--- |
| **Kika Core** | El orquestador que razona, planea y ejecuta acciones. | VPS 2 (Cerebro) |
| **Engram Server** | Base de datos vectorial y motor de búsqueda semántica. | VPS 2 (Localhost) |
| **OpenRouter API** | Acceso a modelos de lenguaje (Claude 3.5, Llama 3, etc.). | Nube (External) |
| **Blink Tunnel** | Túnel blindado para comunicación Celular <-> VPS. | VPS 2 <-> Celular |
| **Action Engine** | Módulo que interactúa con la terminal y el VPS 1. | VPS 2 -> VPS 1 |

## 2. Flujo de Información (El Ciclo de Memoria)

### A. Recepción y Recuperación (Retrieval)
1. **Entrada**: El usuario envía una orden desde el celular o terminal.
2. **Query Semántica**: Kika genera un "embedding" de la orden y consulta a **Engram** (vía HTTP API).
3. **Recuperación**: Engram devuelve los 3-5 recuerdos más relevantes (comandos exitosos pasados, errores previos, documentación técnica).

### B. Razonamiento y Planificación
4. **Enriquecimiento**: Kika construye un prompt "chingón" que incluye:
   - La orden del usuario.
   - Los recuerdos recuperados de Engram.
   - El estado actual del sistema (logs de Nginx, Docker, etc.).
5. **Inferencia**: Se envía el prompt a **OpenRouter**. El modelo genera un plan de acción en formato JSON.

### C. Ejecución y Almacenamiento (Storage)
6. **Acción**: El Action Engine ejecuta los comandos en la terminal.
7. **Validación**: Kika verifica si la acción fue exitosa.
8. **Consolidación**: Kika envía a **Engram** el resumen de la tarea:
   - *Input*: La orden original.
   - *Proceso*: Los comandos ejecutados.
   - *Resultado*: Si funcionó o qué error dio.
   - *Metadatos*: Fecha, etiquetas (nginx, ssl, docker).

## 3. Ventajas de usar Engram
- **Persistencia Real**: Kika no olvida lo que hizo aunque se reinicie el VPS.
- **Aprendizaje Continuo**: Si Kika soluciona un error 502 hoy, mañana sabrá cómo arreglarlo instantáneamente gracias al recuerdo semántico.
- **Eficiencia de Créditos**: Al tener contexto relevante de Engram, los prompts son más precisos y requieren menos "vueltas" con el LLM.

## 4. Próximos Pasos de Implementación
1. Desplegar **Engram Server** en el VPS 2 vía Docker.
2. Crear el cliente `memory_client.py` en `/core` para hablar con la API de Engram.
3. Indexar los documentos iniciales (Prompts de Codex, Scripts de iPhone) en Engram.
