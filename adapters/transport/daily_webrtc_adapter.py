from typing import Any, Optional
from config.logger_config import logger
from core.ports.transport_port import TransportPort


class DailyWebRTCTransportAdapter(TransportPort):
    """
    Adaptador de transporte WebRTC Cloud usando salas de Daily.co.
    Ideal para conectar clientes Web, React, iOS y Android.
    """

    def __init__(
        self,
        room_url: str,
        token: Optional[str] = None,
        bot_name: str = "Aura Bot"
    ):
        self.room_url = room_url
        self.token = token
        self.bot_name = bot_name
        self._transport: Any = None
        self._input: Any = None
        self._output: Any = None
        self._initialize_transport()

    def _initialize_transport(self):
        if not self.room_url:
            from adapters.mock_adapters import MockProcessor
            self._input = MockProcessor("DailyWebRTCInput-Stub")
            self._output = MockProcessor("DailyWebRTCOutput-Stub")
            self._transport = self
            return

        try:
            from pipecat.transports.services.daily import DailyTransport, DailyParams
            logger.info(f"Conectando a sala WebRTC Daily en {self.room_url}...")
            self._transport = DailyTransport(
                room_url=self.room_url,
                token=self.token,
                bot_name=self.bot_name,
                params=DailyParams(
                    audio_in_enabled=True,
                    audio_out_enabled=True,
                    camera_in_enabled=False,
                    camera_out_enabled=False
                )
            )
            self._input = self._transport.input()
            self._output = self._transport.output()
        except Exception as e:
            logger.warning(f"Daily WebRTC inicialización fallback: {e}")
            from adapters.mock_adapters import MockProcessor
            self._input = MockProcessor("DailyWebRTCInput-Fallback")
            self._output = MockProcessor("DailyWebRTCOutput-Fallback")
            self._transport = self

    def get_input(self) -> Any:
        return self._input

    def get_output(self) -> Any:
        return self._output

    def get_transport(self) -> Any:
        return self._transport

    @property
    def provider_name(self) -> str:
        return f"Daily WebRTC ({self.room_url})"
