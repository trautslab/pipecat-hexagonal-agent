import os
from enum import Enum
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class STTProviderType(str, Enum):
    WHISPER_LOCAL = "whisper_local"
    DEEPGRAM = "deepgram"
    MOCK = "mock"


class LLMProviderType(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


class TTSProviderType(str, Enum):
    PIPER_LOCAL = "piper_local"
    CARTESIA = "cartesia"
    ELEVENLABS = "elevenlabs"
    MOCK = "mock"


class TransportProviderType(str, Enum):
    LOCAL_AUDIO = "local_audio"
    DAILY_WEBRTC = "daily_webrtc"
    WEBSOCKET = "websocket"
    MOCK = "mock"


class AppSettings(BaseSettings):
    """
    Configuración global tipada del sistema basada en Pydantic.
    Admite carga automática de variables de entorno desde archivo .env.
    """
    # Identidad y Comportamiento del Agente
    agent_name: str = Field(default="Aura", alias="AGENT_NAME")
    agent_language: str = Field(default="es", alias="AGENT_LANGUAGE")
    agent_system_prompt: str = Field(
        default=(
            "Eres Aura, una ingeniera de software y asistente de voz de élite con capacidades autónomas estilo OpenClaw/Devin. "
            "Operas sobre una Arquitectura Hexagonal y cuentas con herramientas internas de Búsqueda Web en tiempo real y Runtime de Servidores MCP. "
            "\n\n[REGLAS ESTRICTAS DE AUTONOMÍA]:\n"
            "1. NUNCA le pidas al usuario que ejecute comandos en su terminal (como 'npm run...', 'ejecuta en terminal', 'revisa los logs en...'). "
            "2. Si el usuario te pide probar, sincronizar, crear o verificar una herramienta, EJECÚTALA tú misma mediante tus herramientas internas y entrega directamente los resultados de la acción ya ejecutada. "
            "3. Cuando se realice una acción en Google Calendar u otro MCP, confirma el evento, la hora y el resultado con entusiasmo y seguridad sin delegar tareas manuales. "
            "4. Responde siempre en español con concisión, tono natural y profesional para síntesis de voz fluida."
        ),
        alias="AGENT_SYSTEM_PROMPT"
    )

    # Proveedores Activos (Por defecto: Pila 100% Local y Gratuita)
    stt_provider: STTProviderType = Field(default=STTProviderType.WHISPER_LOCAL, alias="STT_PROVIDER")
    llm_provider: LLMProviderType = Field(default=LLMProviderType.OLLAMA, alias="LLM_PROVIDER")
    tts_provider: TTSProviderType = Field(default=TTSProviderType.PIPER_LOCAL, alias="TTS_PROVIDER")
    transport_provider: TransportProviderType = Field(default=TransportProviderType.LOCAL_AUDIO, alias="TRANSPORT_PROVIDER")

    # Configuración de Modelos Locales
    whisper_model_size: str = Field(default="base", alias="WHISPER_MODEL_SIZE")
    ollama_model: str = Field(default="llama3.1:8b", alias="OLLAMA_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434/v1", alias="OLLAMA_BASE_URL")
    piper_voice_name: str = Field(default="es_ES-davefx-medium", alias="PIPER_VOICE_NAME")

    # Claves de API para Proveedores Cloud (Opcionales)
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    deepgram_api_key: str = Field(default="", alias="DEEPGRAM_API_KEY")
    cartesia_api_key: str = Field(default="", alias="CARTESIA_API_KEY")
    elevenlabs_api_key: str = Field(default="", alias="ELEVENLABS_API_KEY")

    # Configuración de Red y Transporte
    daily_room_url: str = Field(default="", alias="DAILY_ROOM_URL")
    daily_token: str = Field(default="", alias="DAILY_TOKEN")
    web_port: int = Field(default=8765, alias="WEB_PORT")
    web_host: str = Field(default="0.0.0.0", alias="WEB_HOST")

    class Config:
        env_file = str(PROJECT_ROOT / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = AppSettings()
