#!/usr/bin/env python3
import subprocess
import json
import os
import sys

class KikaOrchestrator:
    def __init__(self):
        self.vps_ip = "85.239.241.120"
        self.gentle_ai_bin = "/home/dani/go/bin/gentle-ai"
        self.engram_bin = "/home/dani/go/bin/engram"
        print(f"🛡️ Kika Core Initialized on VPS: {self.vps_ip}")

    def query_memory(self, prompt):
        """Consulta la memoria semántica de Engram"""
        try:
            result = subprocess.run(
                [self.engram_bin, "search", prompt],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"No se pudo consultar la memoria: {str(e)}"

    def store_memory(self, memory_text):
        """Guarda un nuevo recuerdo o decisión en Engram"""
        try:
            result = subprocess.run(
                [self.engram_bin, "add", memory_text],
                capture_output=True, text=True, check=True
            )
            return "Memoria consolidada exitosamente."
        except Exception as e:
            return f"Error guardando memoria: {str(e)}"

    def list_agents(self):
        """Lista los adaptadores y agentes soportados por Gentle-AI"""
        try:
            result = subprocess.run(
                [self.gentle_ai_bin, "doctor"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error listando agentes: {str(e)}"

if __name__ == "__main__":
    kika = KikaOrchestrator()
    print("--- Estado del Sistema Gentle-AI ---")
    print(kika.list_agents())
