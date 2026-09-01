from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SearchPort(ABC):
    """
    Puerto abstracto para motores de búsqueda web en tiempo real.
    Permite recuperar evidencias factuales de internet a costo $0 o mediante APIs cloud.
    """

    @abstractmethod
    async def search(self, query: str, max_results: int = 3) -> str:
        """
        Ejecuta una búsqueda web y retorna fragmentos enriquecidos con URLs y texto.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nombre identificativo del proveedor de búsqueda."""
        pass
