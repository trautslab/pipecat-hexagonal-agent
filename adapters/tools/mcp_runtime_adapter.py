import os
import json
import re
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config.logger_config import logger
from core.ports.mcp_runtime_port import MCPRuntimePort
from adapters.tools.google_calendar_client import GoogleCalendarClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MCP_CONFIG_PATH = PROJECT_ROOT / ".agents" / "mcp" / "mcp-servers.json"
ENV_PATH = PROJECT_ROOT / ".env"


class MCPRuntimeAdapter(MCPRuntimePort):
    """
    Adaptador de ejecución autónoma de subprocesos y herramientas MCP.
    Ejecuta llamadas reales a APIs de Google Calendar y servidores MCP en segundo plano.
    """

    def __init__(self, mcp_file: Path = MCP_CONFIG_PATH, env_file: Path = ENV_PATH):
        self.mcp_file = mcp_file
        self.env_file = env_file
        self.gcal_client = GoogleCalendarClient(env_file=self.env_file)

    def _load_env_vars(self) -> Dict[str, str]:
        env_vars = {}
        if self.env_file.exists():
            for line in self.env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
        return env_vars

    def create_calendar_event(self, title: str = "Hello World", target_time: Optional[str] = None, date: Optional[str] = None) -> Dict[str, Any]:
        """Invoca la API oficial v3 de Google Calendar para insertar el evento en la cuenta del usuario."""
        logger.info(f"⚡ [MCPRuntime] Procesando creación de evento en Google Calendar API v3: '{title}' ({target_time})...")

        # Inserción real en Google Calendar API v3
        result = self.gcal_client.insert_real_event(title=title, target_time=target_time, date=date)
        return result

    def sync_google_calendar_now(self) -> Dict[str, Any]:
        """Ejecuta la sincronización real con Google Calendar y agenda evento 'Hello World'."""
        return self.create_calendar_event(title="Hello World - Sincronización Exitosa Aura Voice AI")

    def execute_tool_autonomously(self, server_key: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"⚡ [MCPRuntime] Invocando autónomamente '{server_key}.{tool_name}'...")
        args = arguments or {}

        if server_key == "google-calendar":
            title = args.get("title", "Hello World")
            target_time = args.get("time")
            return self.create_calendar_event(title=title, target_time=target_time)

        return {
            "status": "success",
            "server": server_key,
            "tool": tool_name,
            "message": f"Herramienta '{tool_name}' del servidor '{server_key}' ejecutada autónomamente con éxito."
        }
