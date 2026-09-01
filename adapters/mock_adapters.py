import asyncio
from typing import Any
from config.logger_config import logger
from core.ports.stt_port import STTPort
from core.ports.llm_port import LLMPort
from core.ports.tts_port import TTSPort
from core.ports.transport_port import TransportPort

try:
    from pipecat.processors.frame_processor import FrameProcessor
    from pipecat.frames.frames import Frame, TextFrame, AudioRawFrame
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

    class TextFrame(Frame):
        def __init__(self, text: str):
            self.text = text


class MockProcessor(FrameProcessor):
    """Procesador genérico mock para pruebas unitarias y validación offline."""
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    async def process_frame(self, frame: Any, direction: Any):
        if hasattr(super(), "process_frame"):
            await super().process_frame(frame, direction)
        if hasattr(self, "push_frame"):
            await self.push_frame(frame, direction)


class MockSTTAdapter(STTPort):
    def __init__(self):
        self._service = MockProcessor("MockSTT")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return "Mock STT (Simulación)"


class MockLLMAdapter(LLMPort):
    def __init__(self, system_prompt: str = "Eres un asistente de prueba."):
        self.system_prompt = system_prompt
        self._service = MockProcessor("MockLLM")

    def get_service(self) -> Any:
        return self._service

    def get_system_prompt(self) -> str:
        return self.system_prompt

    @property
    def provider_name(self) -> str:
        return "Mock LLM (Simulación)"


class MockTTSAdapter(TTSPort):
    def __init__(self):
        self._service = MockProcessor("MockTTS")

    def get_service(self) -> Any:
        return self._service

    @property
    def provider_name(self) -> str:
        return "Mock TTS (Simulación)"


class MockTransportAdapter(TransportPort):
    def __init__(self):
        self._input = MockProcessor("MockTransportInput")
        self._output = MockProcessor("MockTransportOutput")

    def get_input(self) -> Any:
        return self._input

    def get_output(self) -> Any:
        return self._output

    def get_transport(self) -> Any:
        return self

    @property
    def provider_name(self) -> str:
        return "Mock Transport (Simulación)"
