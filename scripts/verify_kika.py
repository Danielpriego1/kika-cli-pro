#!/usr/bin/env python3
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:7488"


def request(path, payload=None):
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE_URL + path, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def main():
    marker = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results = {}

    status_code, health = request("/health")
    results["health"] = {
        "http": status_code,
        "status": health.get("status"),
        "registry_agents": health.get("registry_agents"),
        "available_agent_profiles": health.get("available_agent_profiles"),
        "engram_ok": health.get("engram", {}).get("ok"),
    }

    status_code, agents = request("/agents")
    results["agents"] = {
        "http": status_code,
        "count": len(agents.get("agents", [])),
        "unavailable": [agent["id"] for agent in agents.get("agents", []) if not agent.get("available")],
    }

    title = f"Prueba de integracion Kika {marker}"
    message = "Kika-AI confirmo que Engram, la API local y el registro de agentes responden de forma verificable."
    status_code, memory = request("/memory", {"title": title, "message": message, "type": "verification"})
    results["memory_save"] = {"http": status_code, "ok": memory.get("ok"), "project": memory.get("project")}

    status_code, search = request("/memory/search", {"query": title, "limit": 3})
    results["memory_search"] = {"http": status_code, "ok": search.get("ok"), "found_marker": marker in search.get("results", "")}

    status_code, job = request(
        "/dispatch",
        {
            "agent_id": "qa-verifier",
            "objective": "Validar que la nueva API local de Kika responda salud, agentes y memoria.",
            "context": "Trabajo de prueba creado por la integración inicial.",
        },
    )
    results["delegation"] = {
        "http": status_code,
        "job_id": job.get("job_id"),
        "status": job.get("status"),
        "agent": job.get("agent", {}).get("id"),
    }

    print(json.dumps(results, ensure_ascii=False, indent=2))
    failures = []
    if results["health"]["status"] != "healthy":
        failures.append("health")
    if results["agents"]["count"] != 22 or results["agents"]["unavailable"]:
        failures.append("agents")
    if not results["memory_save"]["ok"] or not results["memory_search"]["found_marker"]:
        failures.append("memory")
    if results["delegation"]["status"] != "queued":
        failures.append("delegation")
    if failures:
        print("FAILED: " + ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
