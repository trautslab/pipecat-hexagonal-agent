from typing import Any
from config.logger_config import logger
from core.ports.llm_port import LLMPort


class OllamaLLMAdapter(LLMPort):
    """
    Adaptador de LLM gratuito y local ejecutado con Ollama.
    Aprovecha la compatibilidad de streaming local de Ollama.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        model: str = "llama3.2:3b",
        system_prompt: str = "Eres un asistente de voz conciso y amigable."
    ):
        self.base_url = base_url
        self.model = model
        self.system_prompt = system_prompt
        self._service: Any = None
        self._initialize_service()

    def _initialize_service(self):
        logger.info(f"Conectando con Ollama Local en {self.base_url} (Modelo: {self.model})...")
        try:
            from pipecat.services.ollama import OllamaLLMService
            self._service = OllamaLLMService(
                model=self.model,
                base_url=self.base_url.replace("/v1", "")
            )
        except Exception:
            try:
                from pipecat.services.openai import OpenAILLMService
                self._service = OpenAILLMService(
                    api_key="ollama",
                    base_url=self.base_url,
                    model=self.model
                )
            except Exception:
                from adapters.mock_adapters import MockProcessor
                self._service = MockProcessor(f"OllamaLLM-{self.model}")

    def get_service(self) -> Any:
        return self._service

    def get_system_prompt(self) -> str:
        return self.system_prompt

    @property
    def provider_name(self) -> str:
        return f"Ollama Local ({self.model})"
