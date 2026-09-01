#!/usr/bin/env python3
"""
Telemetry Logger (AI-SDLC Standard)
Registra eventos estructurados del ciclo de vida agéntico en .agents/telemetry/events.jsonl
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path


def log_event(phase: str, task: str, status: str, message: str, metadata: dict = None):
    telemetry_dir = Path(__file__).resolve().parent.parent / ".agents" / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    events_file = telemetry_dir / "events.jsonl"

    event_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "task_id": task,
        "status": status,
        "message": message,
        "metadata": metadata or {}
    }

    with open(events_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_payload, ensure_ascii=False) + "\n")

    print(f"📊 [TELEMETRY] [{phase}] ({task}) -> {status}: {message}")


def main():
    parser = argparse.ArgumentParser(description="AI-SDLC Telemetry Logger")
    parser.add_argument("--phase", default="EXECUTION", help="Fase del ciclo de vida (INGESTION, DESIGN, EXECUTION, EVALUATION, MERGE)")
    parser.add_argument("--task", default="GENERAL", help="ID de Tarea (e.g. TASK-001)")
    parser.add_argument("--status", default="SUCCESS", help="Estado del evento (SUCCESS, FAILED, IN_PROGRESS, INFO)")
    parser.add_argument("--msg", default="", help="Mensaje descriptivo del evento")

    args = parser.parse_args()
    log_event(args.phase, args.task, args.status, args.msg)


if __name__ == "__main__":
    main()
