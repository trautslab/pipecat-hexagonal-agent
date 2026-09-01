from abc import ABC, abstractmethod
from typing import Any, Optional


class LLMPort(ABC):
    """
    Puerto (Interfaz) para el servicio de Large Language Model.
    Cualquier adaptador (Ollama, OpenAI, Claude, Gemini, etc.) debe implementar este contrato.
    """

    @abstractmethod
    def get_service(self) -> Any:
        """
        Retorna la instancia del servicio LLM de Pipecat compatible con el Pipeline.
        """
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Retorna el system prompt configurado para el modelo."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificativo del proveedor LLM."""
        pass
