from abc import ABC, abstractmethod
from typing import Dict, Any


class MCPExecutorPort(ABC):
    """
    Puerto abstracto para validación de credenciales y ejecución activa de herramientas MCP.
    """

    @abstractmethod
    def validate_credentials(self, server_key: str) -> Dict[str, Any]:
        """Verifica el estado de las credenciales en .env para un servidor MCP."""
        pass

    @abstractmethod
    def execute_probe_action(self, server_key: str, action: str = "test_event") -> Dict[str, Any]:
        """Ejecuta una acción de prueba activa en el servidor MCP (ej. crear evento en Google Calendar)."""
        pass
