from abc import ABC, abstractmethod
from typing import Any


class TTSPort(ABC):
    """
    Puerto (Interfaz) para el servicio de Text-To-Speech (Síntesis de Voz).
    Cualquier adaptador (Piper local, Kokoro, Cartesia, ElevenLabs, etc.) debe implementar este contrato.
    """

    @abstractmethod
    def get_service(self) -> Any:
        """
        Retorna la instancia del servicio TTS de Pipecat compatible con el Pipeline.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificativo del proveedor de TTS."""
        pass
