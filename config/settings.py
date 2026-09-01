import os
from enum import Enum
from typing import Optional
from dataclasses import dataclass

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False


class STTProviderType(str, Enum):
    WHISPER_LOCAL = "whisper_local"
    DEEPGRAM = "deepgram"
    MOCK = "mock"


class LLMProviderType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    MOCK = "mock"


class TTSProviderType(str, Enum):
    PIPER_LOCAL = "piper_local"
    CARTESIA = "cartesia"
    MOCK = "mock"


class TransportProviderType(str, Enum):
    LOCAL_AUDIO = "local_audio"
    DAILY_WEBRTC = "daily_webrtc"
    WEBSOCKET = "websocket"
    MOCK = "mock"


DEFAULT_SYSTEM_PROMPT = (
    "Eres Aura, una asistente de voz e ingeniera de software proactiva y resolutiva en español. "
    "Conoces tu propia arquitectura (pipecat-hexagonal-agent), estructurada con Arquitectura Hexagonal: "
    "puertos en core/ports/, adaptadores en adapters/ (incluyendo adapters/tools/ para herramientas), "
    "catálogo MCP en .agents/mcp/mcp-servers.json y variables en .env. "
    "NUNCA te disculpes ni digas 'como asistente de voz no puedo hacer X'. En su lugar, asume tu rol de ingeniera del sistema: "
    "explica de inmediato cómo se integra la funcionalidad o servidor MCP solicitado (como Google Calendar MCP, bases de datos o APIs), "
    "explica los pasos técnicos que se implementarán y dile al usuario con precisión qué credenciales o variables debe colocar en su archivo .env. "
    "Comunícate con claridad, tono profesional, conciso y natural."
)


if HAS_PYDANTIC:
    class AppSettings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )

        stt_provider: STTProviderType = Field(default=STTProviderType.WHISPER_LOCAL, alias="STT_PROVIDER")
        llm_provider: LLMProviderType = Field(default=LLMProviderType.OLLAMA, alias="LLM_PROVIDER")
        tts_provider: TTSProviderType = Field(default=TTSProviderType.PIPER_LOCAL, alias="TTS_PROVIDER")
        transport_provider: TransportProviderType = Field(
            default=TransportProviderType.LOCAL_AUDIO, alias="TRANSPORT_PROVIDER"
        )

        agent_name: str = Field(default="Aura", alias="AGENT_NAME")
        agent_language: str = Field(default="es", alias="AGENT_LANGUAGE")
        agent_system_prompt: str = Field(
            default=DEFAULT_SYSTEM_PROMPT,
            alias="AGENT_SYSTEM_PROMPT"
        )

        whisper_model_size: str = Field(default="base", alias="WHISPER_MODEL_SIZE")
        whisper_device: str = Field(default="auto", alias="WHISPER_DEVICE")

        ollama_base_url: str = Field(default="http://localhost:11434/v1", alias="OLLAMA_BASE_URL")
        ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")

        piper_voice_name: str = Field(default="es_ES-davefx-medium", alias="PIPER_VOICE_NAME")
        piper_model_path: Optional[str] = Field(default=None, alias="PIPER_MODEL_PATH")

        openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
        openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

        deepgram_api_key: Optional[str] = Field(default=None, alias="DEEPGRAM_API_KEY")

        cartesia_api_key: Optional[str] = Field(default=None, alias="CARTESIA_API_KEY")
        cartesia_voice_id: Optional[str] = Field(
            default="79a125e8-cd45-4c13-8a67-188112f4dd22", alias="CARTESIA_VOICE_ID"
        )

        daily_room_url: Optional[str] = Field(default=None, alias="DAILY_ROOM_URL")
        daily_token: Optional[str] = Field(default=None, alias="DAILY_TOKEN")

        web_host: str = Field(default="0.0.0.0", alias="WEB_HOST")
        web_port: int = Field(default=8765, alias="WEB_PORT")

else:
    @dataclass
    class AppSettings:
        stt_provider: STTProviderType = STTProviderType.WHISPER_LOCAL
        llm_provider: LLMProviderType = LLMProviderType.OLLAMA
        tts_provider: TTSProviderType = TTSProviderType.PIPER_LOCAL
        transport_provider: TransportProviderType = TransportProviderType.LOCAL_AUDIO

        agent_name: str = "Aura"
        agent_language: str = "es"
        agent_system_prompt: str = DEFAULT_SYSTEM_PROMPT

        whisper_model_size: str = "base"
        whisper_device: str = "auto"

        ollama_base_url: str = "http://localhost:11434/v1"
        ollama_model: str = "llama3.1:8b"

        piper_voice_name: str = "es_ES-davefx-medium"
        piper_model_path: Optional[str] = None

        openai_api_key: Optional[str] = None
        openai_model: str = "gpt-4o-mini"

        deepgram_api_key: Optional[str] = None

        cartesia_api_key: Optional[str] = None
        cartesia_voice_id: Optional[str] = "79a125e8-cd45-4c13-8a67-188112f4dd22"

        daily_room_url: Optional[str] = None
        daily_token: Optional[str] = None

        web_host: str = "0.0.0.0"
        web_port: int = 8765

        def __init__(self, **kwargs):
            for key, val in kwargs.items():
                attr = key.lower()
                if hasattr(self, attr):
                    setattr(self, attr, val)


settings = AppSettings()
