from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SessionRepositoryPort(ABC):
    """
    Puerto abstracto para la persistencia agnóstica de conversaciones y logs de telemetría en el backend.
    """

    @abstractmethod
    def list_sessions(self) -> List[Dict[str, Any]]:
        """Lista todas las sesiones guardadas."""
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una sesión completa con mensajes y consola por su ID."""
        pass

    @abstractmethod
    def save_session(self, session_data: Dict[str, Any]) -> bool:
        """Guarda o actualiza una sesión de forma atómica."""
        pass

    @abstractmethod
    def append_console_step(self, session_id: str, turn_index: int, step: Dict[str, Any]) -> bool:
        """Agrega un paso de telemetría en tiempo real al turno de la sesión."""
        pass

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión del almacenamiento."""
        pass
