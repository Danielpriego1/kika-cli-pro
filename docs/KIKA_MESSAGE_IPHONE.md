# Kika Message para iPhone

## Propósito

`Kika Message` permite enviar una orden escrita desde el iPhone al orquestador Kika-AI en el VPS. El Atajo utiliza SSH con una clave dedicada y entrega la orden al receptor local de Kika, sin publicar la API del orquestador en Internet.

## Flujo

```text
iPhone / Atajos
  └─ Solicitar texto
      └─ SSH cifrado con clave ed25519
          └─ usuario restringido kika-mobile
              └─ receptor forzado kika-send
                  └─ Kika-AI API local (127.0.0.1:7488)
                      └─ cola de delegación y políticas de aprobación
```

## Configuración final del Atajo

El Atajo contiene tres acciones, en este orden:

1. **Solicitar texto**. Pregunta recomendada: `¿Qué orden le das a Kika?`.
2. **Ejecutar script mediante SSH**. Usa esta configuración:

| Campo | Valor |
|---|---|
| Script | `kika-send` |
| Entrada | Salida de la acción **Solicitar texto** |
| Host | `85.239.241.120` |
| Puerto | `22` |
| Usuario | `kika-mobile` |
| Autenticación | Clave SSH ed25519 creada por Atajos |

3. **Leer resultado del script de shell**. Opcionalmente, puede sustituirse por una acción que extraiga `message` y `job_id` del JSON para mostrar una respuesta más breve.

> El campo **Entrada** debe contener la variable de la orden escrita por el usuario. No debe contener el texto `kika-send`.

## Seguridad aplicada

La clave del iPhone se registra para el usuario `kika-mobile`. La cuenta no posee privilegios administrativos. La clave tiene un comando SSH forzado hacia `/usr/local/lib/kika/kika_ssh_entry.py`, con reenvío de puertos, agente, X11, TTY y configuración de usuario deshabilitados.

El receptor solo acepta el comando original `kika-send`. El texto recibido queda limitado a 1,500 caracteres, se registra como delegación de `kika-coordinator` y queda sujeto a las políticas de aprobación del registro de agentes. No interpreta la orden como código de shell.

## Respuesta esperada

Una entrega correcta devuelve un objeto JSON similar al siguiente:

```json
{
  "ok": true,
  "message": "Orden recibida por Kika.",
  "job_id": "kika-...",
  "status": "pending_approval",
  "agent": "Kika Coordinadora"
}
```

El estado `pending_approval` es esperado para una orden delegada a la coordinadora: deja una trazabilidad y evita que las operaciones sensibles se ejecuten sin revisión.

## Operación y recuperación

Para reemplazar la clave pública del iPhone, guárdala temporalmente en un archivo `.pub` y ejecuta en el VPS:

```bash
sudo /home/dani/kika-cli-pro/scripts/register_kika_mobile_key.sh /ruta/a/clave-publica.pub
```

El script instala el receptor de ejecución como una copia protegida bajo `/usr/local/lib/kika/` y reemplaza la clave anterior. No se deben versionar claves privadas, claves públicas personales ni archivos de la carpeta `integrations/mac/private/`.

## Diagnóstico

| Síntoma | Verificación | Acción |
|---|---|---|
| Error de autenticación SSH | Confirmar que la clave pública actual esté registrada para `kika-mobile`. | Reejecutar `register_kika_mobile_key.sh` con la clave pública que genera Atajos. |
| `Formato de orden inválido` | Revisar el campo **Entrada** del Atajo. | Seleccionar la salida de **Solicitar texto**; no usar un texto fijo. |
| No responde Kika | Revisar el servicio local. | `systemctl status kika-orchestrator.service` y `curl http://127.0.0.1:7488/health`. |
| Error de autorización | Confirmar que Script sea solo `kika-send`. | No agregar `ssh`, `curl`, `bash` ni comandos adicionales. |
