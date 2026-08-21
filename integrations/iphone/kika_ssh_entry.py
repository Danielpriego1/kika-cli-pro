#!/usr/bin/env python3
"""Restricted SSH entrypoint for the iPhone Kika Message shortcut.

The script is intended to be used only as an SSH forced command. It accepts
plain UTF-8 text over standard input (the default Shortcuts path) or a
base64url argument for backward compatibility, records it as a Kika coordinator
delegation and returns compact JSON for Shortcuts. It never evaluates shell
input or executes arbitrary commands.
"""

from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

MOBILE_QUERY_URL = "http://127.0.0.1:7488/mobile/query"
DISPATCH_URL = "http://127.0.0.1:7488/dispatch"
MAX_ORDER_LENGTH = 1500
BASE64URL = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


def reply(payload: dict, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    raise SystemExit(exit_code)


def validate_order(order: str) -> str:
    order = order.strip()
    if not order or len(order) > MAX_ORDER_LENGTH or any(ord(char) < 32 and char not in "\n\t" for char in order):
        reply({"ok": False, "error": "La orden está vacía o excede los límites permitidos."}, 64)
    # Shortcuts can accidentally pass rich-text metadata from a deleted action.
    # Reject it explicitly instead of creating a meaningless approval job.
    if order.startswith("{\\rtf") or "\\cocoatextscaling" in order:
        reply(
            {
                "ok": False,
                "error": "El Atajo envió texto técnico de una acción anterior. En la acción SSH, selecciona como Entrada la salida de Solicitar texto.",
            },
            64,
        )
    return order


def decode_order(command: str) -> str:
    parts = command.strip().split()
    if parts == ["kika-send"]:
        return validate_order(sys.stdin.read(MAX_ORDER_LENGTH + 1))
    if len(parts) != 2 or parts[0] != "kika-send":
        reply(
            {
                "ok": False,
                "error": "Comando no autorizado. Usa exclusivamente kika-send.",
            },
            64,
        )
    encoded = parts[1]
    if len(encoded) > 4096 or not BASE64URL.fullmatch(encoded):
        reply({"ok": False, "error": "Formato de orden inválido."}, 64)
    try:
        padded = encoded + "=" * (-len(encoded) % 4)
        return validate_order(base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        reply({"ok": False, "error": "No se pudo decodificar la orden."}, 64)


def post_json(url: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        reply({"ok": False, "error": f"Kika devolvió HTTP {error.code}."}, 70)
    except (urllib.error.URLError, TimeoutError):
        reply({"ok": False, "error": "Kika no respondió. Revisa el servicio."}, 70)
    except json.JSONDecodeError:
        reply({"ok": False, "error": "Respuesta inválida de Kika."}, 70)
    if not isinstance(body, dict):
        reply({"ok": False, "error": "Respuesta inválida de Kika."}, 70)
    return body


def submit(order: str) -> None:
    query_result = post_json(MOBILE_QUERY_URL, {"query": order})
    if query_result.get("handled"):
        reply(
            {
                "ok": True,
                "message": query_result.get("message", "Consulta completada."),
                "status": query_result.get("status", "completed"),
                "kind": "read_only_query",
                "data": query_result.get("data", {}),
            }
        )

    dispatch_result = post_json(
        DISPATCH_URL,
        {
            "agent_id": "kika-coordinator",
            "objective": "Orden recibida desde iPhone: " + order,
            "context": "Canal: Atajo Kika Message mediante SSH restringido. La orden debe seguir las reglas de aprobación del registro de agentes.",
        },
    )
    reply(
        {
            "ok": True,
            "message": "Orden recibida por Kika; requiere revisión antes de ejecutarse.",
            "job_id": dispatch_result.get("job_id"),
            "status": dispatch_result.get("status"),
            "kind": "approval_queue",
            "agent": dispatch_result.get("agent", {}).get("name", "Kika Coordinadora"),
        }
    )


def main() -> None:
    original_command = os.environ.get("SSH_ORIGINAL_COMMAND", "")
    submit(decode_order(original_command))


if __name__ == "__main__":
    main()
