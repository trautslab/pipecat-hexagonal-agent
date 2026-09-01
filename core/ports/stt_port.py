from abc import ABC, abstractmethod
from typing import Any


class STTPort(ABC):
    """
    Puerto (Interfaz) para el servicio de Speech-To-Text (Reconocimiento de Voz).
    Cualquier adaptador (Whisper Local, Deepgram, Azure, etc.) debe implementar este contrato.
    """

    @abstractmethod
    def get_service(self) -> Any:
        """
        Retorna la instancia del servicio de Pipecat compatible con el Pipeline.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificativo del proveedor de STT."""
        pass
