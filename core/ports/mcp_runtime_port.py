from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MCPRuntimePort(ABC):
    """
    Puerto abstracto para la ejecución autónoma de subprocesos y herramientas MCP.
    """

    @abstractmethod
    def execute_tool_autonomously(self, server_key: str, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Ejecuta directamente una herramienta MCP sin delegar comandos al usuario."""
        pass

    @abstractmethod
    def sync_google_calendar_now(self) -> Dict[str, Any]:
        """Ejecuta la sincronización inmediata de Google Calendar y crea un evento de prueba en 1 minuto."""
        pass
