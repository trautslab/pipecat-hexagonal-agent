from typing import Any
from config.logger_config import logger
from core.ports.transport_port import TransportPort


class LocalAudioTransportAdapter(TransportPort):
    """
    Adaptador de transporte local de audio (Micrófono y Parlantes del ordenador).
    No requiere servidores WebRTC ni infraestructura externa (Costo $0).
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self._transport: Any = None
        self._input: Any = None
        self._output: Any = None
        self._initialize_transport()

    def _initialize_transport(self):
        logger.info("Inicializando transporte de Audio Local (Micrófono/Altavoz del sistema)...")
        try:
            from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioParams
            self._transport = LocalAudioTransport(
                params=LocalAudioParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    audio_in_sample_rate=self.sample_rate,
                    audio_out_sample_rate=self.sample_rate
                )
            )
            self._input = self._transport.input()
            self._output = self._transport.output()
        except Exception as e:
            logger.warning(f"Local audio hardware fallback: {e}")
            from adapters.mock_adapters import MockProcessor
            self._input = MockProcessor("LocalAudioInput")
            self._output = MockProcessor("LocalAudioOutput")
            self._transport = self

    def get_input(self) -> Any:
        return self._input

    def get_output(self) -> Any:
        return self._output

    def get_transport(self) -> Any:
        return self._transport

    @property
    def provider_name(self) -> str:
        return "Local Audio (Mic & Speakers)"
