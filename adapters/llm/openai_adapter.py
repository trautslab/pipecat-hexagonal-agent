from typing import Any
from config.logger_config import logger
from core.ports.llm_port import LLMPort


class OpenAILLMAdapter(LLMPort):
    """
    Adaptador de LLM Cloud usando OpenAI (ej. GPT-4o, GPT-4o-mini).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        system_prompt: str = "Eres un asistente de voz conciso y amigable."
    ):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        if not self.api_key:
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor(f"OpenAILLM-{self.model}-Stub")
            return

        try:
            from pipecat.services.openai import OpenAILLMService
            logger.info(f"Inicializando OpenAI LLM Cloud (Modelo: {self.model})...")
            self._service = OpenAILLMService(
                api_key=self.api_key,
                model=self.model
            )
        except Exception as e:
            logger.warning(f"OpenAI LLM inicialización fallback: {e}")
            from adapters.mock_adapters import MockProcessor
            self._service = MockProcessor(f"OpenAILLM-{self.model}-Fallback")

    def get_service(self) -> Any:
        return self._service

    def get_system_prompt(self) -> str:
        return self.system_prompt

    @property
    def provider_name(self) -> str:
        return f"OpenAI ({self.model})"
