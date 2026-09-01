from typing import Any
from config.logger_config import logger
from core.ports.stt_port import STTPort


class DeepgramSTTAdapter(STTPort):
    """
    Adaptador de STT Cloud usando Deepgram.
    """

    def __init__(self, api_key: str, language: str = "es"):
        self.api_key = api_key
        self.language = language
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        if not self.api_key:
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor("DeepgramSTT-Stub")
            return
        
        try:
            from pipecat.services.deepgram import DeepgramSTTService
            logger.info("Inicializando Deepgram STT Cloud...")
            self._service = DeepgramSTTService(
                api_key=self.api_key,
                language=self.language
            )
        except Exception as e:
            logger.warning(f"Deepgram STT inicialización fallback: {e}")
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor("DeepgramSTT-Fallback")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return "Deepgram (Cloud)"
