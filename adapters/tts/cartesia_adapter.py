from typing import Any, Optional
from config.logger_config import logger
from core.ports.tts_port import TTSPort


class CartesiaTTSAdapter(TTSPort):
    """
    Adaptador de TTS Cloud usando Cartesia Sonic (Voz natural en tiempo real).
    """

    def __init__(
        self,
        api_key: str,
        voice_id: str = "79a125e8-cd45-4c13-8a67-188112f4dd22"
    ):
        self.api_key = api_key
        self.voice_id = voice_id
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        if not self.api_key:
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor("CartesiaTTS-Stub")
            return

        try:
            from pipecat.services.cartesia import CartesiaTTSService
            logger.info(f"Inicializando Cartesia TTS Cloud (Voice ID: {self.voice_id})...")
            self._service = CartesiaTTSService(
                api_key=self.api_key,
                voice_id=self.voice_id
            )
        except Exception as e:
            logger.warning(f"Cartesia TTS inicialización fallback: {e}")
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor("CartesiaTTS-Fallback")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return f"Cartesia (Cloud - {self.voice_id[:8]}...)"
