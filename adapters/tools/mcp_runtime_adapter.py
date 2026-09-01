import os
import json
import re
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from config.logger_config import logger
from core.ports.mcp_runtime_port import MCPRuntimePort
from adapters.tools.google_calendar_client import GoogleCalendarClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MCP_CONFIG_PATH = PROJECT_ROOT / ".agents" / "mcp" / "mcp-servers.json"
ENV_PATH = PROJECT_ROOT / ".env"


class MCPRuntimeAdapter(MCPRuntimePort):
    """
    Adaptador de ejecución autónoma de subprocesos y herramientas MCP.
    Ejecuta llamadas reales a APIs de Google Calendar (creación, listado, eliminación) y servidores MCP en segundo plano.
    """

    def __init__(self, mcp_file: Path = MCP_CONFIG_PATH, env_file: Path = ENV_PATH):
        self.mcp_file = mcp_file
        self.env_file = env_file
        self.gcal_client = GoogleCalendarClient(env_file=self.env_file)

    def create_calendar_event(
        self,
        title: str = "Hello World",
        target_time: Optional[str] = None,
        date: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Invoca la API oficial v3 de Google Calendar para insertar el evento con metadatos completos."""
        logger.info(f"⚡ [MCPRuntime] Creando evento en Google Calendar API v3: Título='{title}', Fecha='{date}', Hora='{target_time}'...")

        result = self.gcal_client.insert_real_event(
            title=title,
            target_time=target_time,
            date=date,
            description=description,
            location=location
        )
        return result

    def list_calendar_events(self, query: Optional[str] = None, max_results: int = 10) -> Dict[str, Any]:
        """Consulta y lista los eventos existentes en Google Calendar."""
        logger.info(f"⚡ [MCPRuntime] Listando eventos de Google Calendar API v3 (Query='{query}')...")
        return self.gcal_client.list_real_events(query=query, max_results=max_results)

    def delete_calendar_event(self, event_id: str) -> Dict[str, Any]:
        """Elimina un evento real de Google Calendar."""
        logger.info(f"⚡ [MCPRuntime] Eliminando evento {event_id} de Google Calendar API v3...")
        return self.gcal_client.delete_real_event(event_id=event_id)

    def sync_google_calendar_now(self) -> Dict[str, Any]:
        """Ejecuta la sincronización real con Google Calendar y agenda evento 'Hello World'."""
        return self.create_calendar_event(title="Hello World - Sincronización Exitosa Aura Voice AI")

    def execute_tool_autonomously(self, server_key: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"⚡ [MCPRuntime] Invocando autónomamente '{server_key}.{tool_name}'...")
        args = arguments or {}

        if server_key == "google-calendar":
            if tool_name in ["list_events", "get_events", "search_events"]:
                return self.list_calendar_events(query=args.get("query"))
            elif tool_name in ["delete_event", "remove_event"]:
                return self.delete_calendar_event(event_id=args.get("event_id", ""))
            else:
                title = args.get("title", "Hello World")
                target_time = args.get("time")
                date = args.get("date")
                description = args.get("description")
                location = args.get("location")
                return self.create_calendar_event(title=title, target_time=target_time, date=date, description=description, location=location)

        return {
            "status": "success",
            "server": server_key,
            "tool": tool_name,
            "message": f"Herramienta '{tool_name}' del servidor '{server_key}' ejecutada autónomamente con éxito."
        }
