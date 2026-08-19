#!/usr/bin/env python3
"""Kika-AI core orchestrator.

The service is deliberately bound to localhost. It stores verified operational
memory in Engram, validates the 22 registered specialist profiles and writes
structured delegation jobs without executing arbitrary user-supplied commands.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(os.getenv("KIKA_PROJECT_ROOT", "/home/dani/kika-cli-pro"))
CONFIG_DIR = PROJECT_ROOT / "config"
REGISTRY_PATH = CONFIG_DIR / "agent_registry.json"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
QUEUE_DIR = RUNTIME_DIR / "queue"
LOG_DIR = PROJECT_ROOT / "logs"
PROJECT_NAME = os.getenv("KIKA_ENGRAM_PROJECT", "kika-cli-pro")
ENGRAM_BIN = os.getenv("ENGRAM_BIN", "/usr/local/bin/engram")
EXPECTED_AGENT_COUNT = 22


class KikaError(RuntimeError):
    """Raised for controlled operational errors."""


class KikaOrchestrator:
    def __init__(self) -> None:
        self._registry_lock = threading.Lock()
        self._ensure_directories()
        self.registry = self._load_registry()

    def _ensure_directories(self) -> None:
        for directory in (CONFIG_DIR, RUNTIME_DIR, QUEUE_DIR, LOG_DIR):
            directory.mkdir(parents=True, exist_ok=True)

    def _load_registry(self) -> dict[str, Any]:
        if not REGISTRY_PATH.exists():
            raise KikaError(f"No existe el registro de agentes: {REGISTRY_PATH}")
        with REGISTRY_PATH.open("r", encoding="utf-8") as source:
            registry = json.load(source)
        agents = registry.get("agents", [])
        ids = [agent.get("id") for agent in agents]
        if len(agents) != EXPECTED_AGENT_COUNT:
            raise KikaError(
                f"El registro debe tener {EXPECTED_AGENT_COUNT} agentes; contiene {len(agents)}."
            )
        if len(ids) != len(set(ids)) or not all(ids):
            raise KikaError("El registro de agentes contiene identificadores vacíos o repetidos.")
        return registry

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _safe_text(value: Any, field: str, limit: int = 6000) -> str:
        if not isinstance(value, str):
            raise KikaError(f"{field} debe ser texto.")
        normalized = value.strip()
        if not normalized:
            raise KikaError(f"{field} no puede estar vacío.")
        if len(normalized) > limit:
            raise KikaError(f"{field} excede el límite de {limit} caracteres.")
        return normalized

    def _run(self, command: list[str], timeout: int = 12) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "ENGRAM_PROJECT": PROJECT_NAME},
        )

    def _engram_health(self) -> dict[str, Any]:
        result = self._run([ENGRAM_BIN, "doctor", "--project", PROJECT_NAME], timeout=15)
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "summary": (result.stdout or result.stderr).strip()[-1800:],
        }

    def runtime_status(self, runtime: str) -> dict[str, Any]:
        if runtime == "engram":
            check = self._engram_health()
            return {"runtime": runtime, "available": check["ok"], "details": check["summary"]}
        executable = shutil.which(runtime)
        if not executable:
            return {"runtime": runtime, "available": False, "details": "Ejecutable no encontrado en PATH."}
        probe = self._run([executable, "--version"], timeout=10)
        return {
            "runtime": runtime,
            "available": probe.returncode == 0,
            "path": executable,
            "details": (probe.stdout or probe.stderr).strip()[:500],
        }

    def agent_statuses(self) -> list[dict[str, Any]]:
        # Multiple profiles can share a runtime. Probe each executable once so
        # health checks remain fast even when all 22 profiles are enabled.
        runtime_cache: dict[str, dict[str, Any]] = {}
        statuses: list[dict[str, Any]] = []
        for agent in self.registry["agents"]:
            runtime_name = agent["runtime"]
            if runtime_name not in runtime_cache:
                runtime_cache[runtime_name] = self.runtime_status(runtime_name)
            runtime = runtime_cache[runtime_name]
            statuses.append(
                {
                    "id": agent["id"],
                    "name": agent["name"],
                    "runtime": runtime_name,
                    "available": runtime["available"],
                    "capabilities": agent["capabilities"],
                    "requires_approval": agent["requires_approval"],
                }
            )
        return statuses

    def health(self) -> dict[str, Any]:
        agent_statuses = self.agent_statuses()
        available_agents = sum(1 for agent in agent_statuses if agent["available"])
        engram = self._engram_health()
        result = {
            "service": "kika-ai",
            "project": PROJECT_NAME,
            "timestamp": self._now(),
            "registry_agents": len(agent_statuses),
            "available_agent_profiles": available_agents,
            "engram": engram,
            "queue_pending": len(list(QUEUE_DIR.glob("*.json"))),
            "status": "healthy" if engram["ok"] and available_agents == EXPECTED_AGENT_COUNT else "degraded",
        }
        self._write_runtime_state(result)
        return result

    def _write_runtime_state(self, state: dict[str, Any]) -> None:
        state_path = RUNTIME_DIR / "status.json"
        temporary = state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(state_path)

    def find_agent(self, agent_id: str) -> dict[str, Any]:
        requested = self._safe_text(agent_id, "agent_id", limit=80)
        for agent in self.registry["agents"]:
            if agent["id"] == requested:
                return agent
        raise KikaError(f"Agente no registrado: {requested}")

    def store_memory(self, title: str, message: str, memory_type: str = "decision") -> dict[str, Any]:
        clean_title = self._safe_text(title, "title", 180)
        clean_message = self._safe_text(message, "message")
        clean_type = self._safe_text(memory_type, "memory_type", 60)
        result = self._run(
            [
                ENGRAM_BIN,
                "save",
                clean_title,
                clean_message,
                "--type",
                clean_type,
                "--project",
                PROJECT_NAME,
            ],
            timeout=20,
        )
        if result.returncode != 0:
            raise KikaError((result.stderr or result.stdout or "Engram no pudo guardar la memoria.").strip())
        return {"ok": True, "title": clean_title, "project": PROJECT_NAME, "details": result.stdout.strip()}

    def search_memory(self, query: str, limit: int = 8) -> dict[str, Any]:
        clean_query = self._safe_text(query, "query", 1200)
        safe_limit = max(1, min(int(limit), 20))
        result = self._run(
            [ENGRAM_BIN, "search", clean_query, "--project", PROJECT_NAME, "--limit", str(safe_limit)],
            timeout=20,
        )
        if result.returncode != 0:
            raise KikaError((result.stderr or result.stdout or "Engram no pudo buscar memoria.").strip())
        return {"ok": True, "project": PROJECT_NAME, "results": result.stdout.strip()}

    def queue_delegation(self, agent_id: str, objective: str, context: str = "") -> dict[str, Any]:
        agent = self.find_agent(agent_id)
        clean_objective = self._safe_text(objective, "objective", 4000)
        clean_context = context.strip() if isinstance(context, str) else ""
        runtime = self.runtime_status(agent["runtime"])
        if not runtime["available"]:
            raise KikaError(f"El runtime {agent['runtime']} para {agent_id} no está disponible.")
        job = {
            "job_id": f"kika-{uuid.uuid4().hex}",
            "created_at": self._now(),
            "status": "pending_approval" if agent["requires_approval"] else "queued",
            "agent": {key: agent[key] for key in ("id", "name", "runtime", "role", "capabilities", "requires_approval")},
            "objective": clean_objective,
            "context": clean_context[:6000],
            "execution_policy": "No se ejecutan comandos arbitrarios desde la API. Cada trabajo debe ser revisado y enviado mediante un runner con parámetros explícitos.",
        }
        target = QUEUE_DIR / f"{job['job_id']}.json"
        target.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.store_memory(
            f"Delegación {agent['id']}",
            f"Trabajo {job['job_id']} registrado para {agent['name']}: {clean_objective}",
            memory_type="task",
        )
        return job


class KikaRequestHandler(BaseHTTPRequestHandler):
    orchestrator: KikaOrchestrator

    def log_message(self, format: str, *args: Any) -> None:
        message = f"{self.address_string()} - {format % args}\n"
        with (LOG_DIR / "kika-api.log").open("a", encoding="utf-8") as log:
            log.write(f"{datetime.now().isoformat()} {message}")

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 12000:
            raise KikaError("El cuerpo JSON debe tener entre 1 y 12000 bytes.")
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(data, dict):
            raise KikaError("El cuerpo debe ser un objeto JSON.")
        return data

    def do_GET(self) -> None:
        try:
            if self.path == "/health":
                self._send_json(HTTPStatus.OK, self.orchestrator.health())
            elif self.path == "/agents":
                self._send_json(HTTPStatus.OK, {"agents": self.orchestrator.agent_statuses()})
            elif self.path == "/status":
                self._send_json(HTTPStatus.OK, self.orchestrator.health())
            else:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})
        except Exception as error:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(error)})

    def do_POST(self) -> None:
        try:
            body = self._read_json()
            if self.path == "/memory":
                result = self.orchestrator.store_memory(
                    body.get("title", ""), body.get("message", ""), body.get("type", "decision")
                )
            elif self.path == "/memory/search":
                result = self.orchestrator.search_memory(body.get("query", ""), body.get("limit", 8))
            elif self.path == "/dispatch":
                result = self.orchestrator.queue_delegation(
                    body.get("agent_id", ""), body.get("objective", ""), body.get("context", "")
                )
            else:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})
                return
            self._send_json(HTTPStatus.OK, result)
        except (KikaError, ValueError, json.JSONDecodeError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception as error:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(error)})


def run_server(orchestrator: KikaOrchestrator) -> None:
    host = os.getenv("KIKA_HOST", "127.0.0.1")
    port = int(os.getenv("KIKA_PORT", "7488"))
    KikaRequestHandler.orchestrator = orchestrator
    server = ThreadingHTTPServer((host, port), KikaRequestHandler)
    print(f"Kika-AI escuchando en http://{host}:{port}", flush=True)
    server.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="Kika-AI Core Orchestrator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("serve", help="Inicia el API local persistente.")
    subparsers.add_parser("status", help="Muestra la salud de Kika.")
    subparsers.add_parser("agents", help="Muestra los 22 agentes y sus runtimes.")
    save_parser = subparsers.add_parser("memory-save", help="Guarda memoria verificada en Engram.")
    save_parser.add_argument("title")
    save_parser.add_argument("message")
    save_parser.add_argument("--type", default="decision")
    search_parser = subparsers.add_parser("memory-search", help="Busca memoria semántica.")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=8)
    dispatch_parser = subparsers.add_parser("dispatch", help="Registra una delegación de un especialista.")
    dispatch_parser.add_argument("agent_id")
    dispatch_parser.add_argument("objective")
    dispatch_parser.add_argument("--context", default="")
    args = parser.parse_args()

    try:
        kika = KikaOrchestrator()
        if args.command == "serve":
            run_server(kika)
        elif args.command == "status":
            print(json.dumps(kika.health(), ensure_ascii=False, indent=2))
        elif args.command == "agents":
            print(json.dumps({"agents": kika.agent_statuses()}, ensure_ascii=False, indent=2))
        elif args.command == "memory-save":
            print(json.dumps(kika.store_memory(args.title, args.message, args.type), ensure_ascii=False, indent=2))
        elif args.command == "memory-search":
            print(json.dumps(kika.search_memory(args.query, args.limit), ensure_ascii=False, indent=2))
        elif args.command == "dispatch":
            print(json.dumps(kika.queue_delegation(args.agent_id, args.objective, args.context), ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        print(f"Kika-AI error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
