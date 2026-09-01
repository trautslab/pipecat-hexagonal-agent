from typing import Any
from config.logger_config import logger
from core.ports.stt_port import STTPort


class WhisperLocalSTTAdapter(STTPort):
    """
    Adaptador de STT gratuito y local usando Faster-Whisper / Whisper en Pipecat.
    """

    def __init__(self, model_size: str = "base", device: str = "auto"):
        self.model_size = model_size
        self.device = device
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        try:
            from pipecat.services.whisper import WhisperSTTService
            logger.info(f"Cargando Whisper Local (modelo: {self.model_size}, device: {self.device})...")
            self._service = WhisperSTTService(
                model=self.model_size,
                device=self.device if self.device != "auto" else None
            )
        except Exception as e:
            logger.warning(f"Whisper STT inicialización fallback: {e}")
            try:
                from pipecat.services.whisper import WhisperSTTService
                self._service = WhisperSTTService(model=self.model_size)
            except Exception:
                from adapters.mock_adapters import MockProcessor
                self._service = MockProcessor(f"WhisperLocal-{self.model_size}")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return f"WhisperLocal (Model: {self.model_size})"
