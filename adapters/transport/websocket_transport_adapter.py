import asyncio
import json
from typing import Any, Optional
from config.logger_config import logger
from core.ports.transport_port import TransportPort

try:
    from pipecat.processors.frame_processor import FrameProcessor
    from pipecat.frames.frames import Frame, AudioRawFrame, TextFrame
except ImportError:
    class FrameProcessor:
        def __init__(self):
            pass
        async def process_frame(self, frame: Any, direction: Any):
            pass
        async def push_frame(self, frame: Any, direction: Any):
            pass

    class Frame:
        pass

    class AudioRawFrame(Frame):
        def __init__(self, audio: bytes, sample_rate: int = 16000, num_channels: int = 1):
            self.audio = audio
            self.sample_rate = sample_rate
            self.num_channels = num_channels

    class TextFrame(Frame):
        def __init__(self, text: str):
            self.text = text


class WebSocketInputProcessor(FrameProcessor):
    """Procesador que recibe audio del cliente WebSocket y lo inyecta al pipeline."""
    def __init__(self, sample_rate: int = 16000):
        super().__init__()
        self.sample_rate = sample_rate

    async def push_audio_chunk(self, chunk: bytes):
        frame = AudioRawFrame(audio=chunk, sample_rate=self.sample_rate, num_channels=1)
        if hasattr(self, "push_frame"):
            await self.push_frame(frame, None)


class WebSocketOutputProcessor(FrameProcessor):
    """Procesador que intercepta audio y texto del pipeline y los envía al cliente WebSocket."""
    def __init__(self, ws_connection=None):
        super().__init__()
        self.ws = ws_connection

    def set_websocket(self, ws):
        self.ws = ws

    async def process_frame(self, frame: Any, direction: Any):
        if hasattr(super(), "process_frame"):
            await super().process_frame(frame, direction)

        if self.ws is not None:
            try:
                # Si es audio, enviamos bytes binarios
                if hasattr(frame, "audio"):
                    if hasattr(self.ws, "send_bytes"):
                        await self.ws.send_bytes(frame.audio)
                    elif hasattr(self.ws, "send"):
                        await self.ws.send(frame.audio)
                # Si es texto (subtítulo / transcripción), enviamos JSON estructurado
                elif hasattr(frame, "text"):
                    payload = json.dumps({"type": "caption", "text": frame.text})
                    if hasattr(self.ws, "send_str"):
                        await self.ws.send_str(payload)
                    elif hasattr(self.ws, "send"):
                        await self.ws.send(payload)
            except Exception as e:
                logger.warning(f"Error enviando frame por WebSocket: {e}")

        if hasattr(self, "push_frame"):
            await self.push_frame(frame, direction)


class WebSocketTransportAdapter(TransportPort):
    """
    Adaptador de transporte por WebSocket bidireccional en tiempo real.
    Permite la conexión de clientes web desde cualquier navegador.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self._input_processor = WebSocketInputProcessor(sample_rate=self.sample_rate)
        self._output_processor = WebSocketOutputProcessor()

    def attach_websocket(self, ws):
        """Asigna la conexión WebSocket activa al procesador de salida."""
        self._output_processor.set_websocket(ws)

    async def handle_incoming_bytes(self, chunk: bytes):
        """Alimenta el procesador de entrada con datos del cliente web."""
        await self._input_processor.push_audio_chunk(chunk)

    def get_input(self) -> Any:
        return self._input_processor

    def get_output(self) -> Any:
        return self._output_processor

    def get_transport(self) -> Any:
        return self

    @property
    def provider_name(self) -> str:
        return "WebSocket Streaming (Web Client)"
