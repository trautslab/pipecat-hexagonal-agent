from abc import ABC, abstractmethod
from typing import Any


class TransportPort(ABC):
    """
    Puerto (Interfaz) para el transporte de Audio/Video.
    Cualquier adaptador (Micrófono/Altavoz Local, Daily WebRTC, WebSockets) debe implementar este contrato.
    """

    @abstractmethod
    def get_input(self) -> Any:
        """Retorna el componente de entrada de audio/frames de Pipecat."""
        pass

    @abstractmethod
    def get_output(self) -> Any:
        """Retorna el componente de salida de audio/frames de Pipecat."""
        pass

    @abstractmethod
    def get_transport(self) -> Any:
        """Retorna la instancia del objeto de transporte subyacente si es requerida."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificativo del transporte."""
        pass
