#!/usr/bin/env python3
"""
Simple MCP Server for introspecting agent architecture and active configuration.
"""
import sys
import json
from pathlib import Path

# Añadir raíz
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import settings


def handle_request():
    status = {
        "status": "ready",
        "agent_name": settings.agent_name,
        "stt": settings.stt_provider,
        "llm": settings.llm_provider,
        "tts": settings.tts_provider,
        "transport": settings.transport_provider
    }
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    handle_request()
