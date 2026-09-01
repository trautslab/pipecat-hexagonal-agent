from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class MCPPort(ABC):
    """
    Puerto abstracto para la gestión y descubrimiento dinámico de herramientas MCP.
    """

    @abstractmethod
    def is_mcp_intent(self, text: str) -> Optional[str]:
        """Detecta si la consulta del usuario solicita instalar o usar una herramienta MCP."""
        pass

    @abstractmethod
    def install_or_configure_mcp(self, server_key: str) -> Dict[str, Any]:
        """Registra el MCP en mcp-servers.json y declara las variables en .env."""
        pass

    @abstractmethod
    def get_installed_servers(self) -> Dict[str, Any]:
        """Obtiene el diccionario de servidores MCP actualmente registrados."""
        pass
