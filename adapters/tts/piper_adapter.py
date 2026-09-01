from typing import Any, Optional
from config.logger_config import logger
from core.ports.tts_port import TTSPort


class PiperLocalTTSAdapter(TTSPort):
    """
    Adaptador de TTS gratuito y local usando Piper TTS en Pipecat.
    Ofrece síntesis offline de ultra-baja latencia.
    """

    def __init__(
        self,
        voice_name: str = "es_ES-davefx-medium",
        model_path: Optional[str] = None
    ):
        self.voice_name = voice_name
        self.model_path = model_path
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        logger.info(f"Cargando Piper TTS Local (Voz: {self.voice_name})...")
        try:
            from pipecat.services.piper import PiperTTSService
            self._service = PiperTTSService(
                voice=self.voice_name,
                model_path=self.model_path
            )
        except Exception as e:
            logger.warning(f"Piper TTS fallback: {e}")
            try:
                from pipecat.services.kokoro import KokoroTTSService
                self._service = KokoroTTSService(voice=self.voice_name)
            except Exception:
                from adapters.mock_adapters import MockProcessor
                self._service = MockProcessor(f"PiperLocalTTS-{self.voice_name}")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return f"PiperTTS Local ({self.voice_name})"
