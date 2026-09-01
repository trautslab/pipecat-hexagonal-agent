import os
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field

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


def _load_env_dict() -> dict:
    env_file = PROJECT_ROOT / ".env"
    env_vars = {}
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars


_ENV = _load_env_dict()


@dataclass
class AppSettings:
    """
    Configuración global tipada del sistema compatible con biblioteca estándar y Pydantic.
    Carga variables de entorno de .env automáticamente con costo $0 de dependencias.
    """
    # Identidad y Comportamiento del Agente
    agent_name: str = _ENV.get("AGENT_NAME", "Aura")
    agent_language: str = _ENV.get("AGENT_LANGUAGE", "es")
    agent_system_prompt: str = _ENV.get(
        "AGENT_SYSTEM_PROMPT",
        (
            "Eres Aura, una asistente e ingeniera de software de élite del proyecto pipecat-hexagonal-agent. "
            "Operas sobre una Arquitectura Hexagonal estricta estructurada en 'core/ports/' y 'adapters/', "
            "y cuentas con herramientas internas de Búsqueda Web en tiempo real y Runtime de Servidores MCP. "
            "\n\n[REGLAS ESTRICTAS DE AUTONOMÍA]:\n"
            "1. NUNCA le pidas al usuario que ejecute comandos en su terminal (como 'npm run...', 'ejecuta en terminal', 'revisa los logs en...'). "
            "2. Si el usuario te pide probar, sincronizar, crear o verificar una herramienta, EJECÚTALA tú misma mediante tus herramientas internas y entrega directamente los resultados de la acción ya ejecutada. "
            "3. Cuando se realice una acción en Google Calendar u otro MCP, confirma el evento, la hora y el resultado con entusiasmo y seguridad sin delegar tareas manuales. "
            "4. Responde siempre en español con concisión, tono natural y profesional para síntesis de voz fluida."
        )
    )

    # Proveedores Activos (Por defecto: Pila 100% Local y Gratuita)
    stt_provider: STTProviderType = STTProviderType(_ENV.get("STT_PROVIDER", STTProviderType.WHISPER_LOCAL.value))
    llm_provider: LLMProviderType = LLMProviderType(_ENV.get("LLM_PROVIDER", LLMProviderType.OLLAMA.value))
    tts_provider: TTSProviderType = TTSProviderType(_ENV.get("TTS_PROVIDER", TTSProviderType.PIPER_LOCAL.value))
    transport_provider: TransportProviderType = TransportProviderType(_ENV.get("TRANSPORT_PROVIDER", TransportProviderType.LOCAL_AUDIO.value))

    # Configuración de Modelos Locales
    whisper_model_size: str = _ENV.get("WHISPER_MODEL_SIZE", "base")
    whisper_device: str = _ENV.get("WHISPER_DEVICE", "cpu")
    ollama_model: str = _ENV.get("OLLAMA_MODEL", "llama3.1:8b")
    ollama_base_url: str = _ENV.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    piper_voice_name: str = _ENV.get("PIPER_VOICE_NAME", "es_ES-davefx-medium")
    piper_model_path: str = _ENV.get("PIPER_MODEL_PATH", "")

    # Claves de API para Proveedores Cloud (Opcionales)
    openai_api_key: str = _ENV.get("OPENAI_API_KEY", "")
    openai_model: str = _ENV.get("OPENAI_MODEL", "gpt-4o-mini")
    deepgram_api_key: str = _ENV.get("DEEPGRAM_API_KEY", "")
    deepgram_model: str = _ENV.get("DEEPGRAM_MODEL", "nova-2-general")
    cartesia_api_key: str = _ENV.get("CARTESIA_API_KEY", "")
    cartesia_voice_id: str = _ENV.get("CARTESIA_VOICE_ID", "79a125e8-cd45-4c13-8a67-188112f4dd22")
    cartesia_model: str = _ENV.get("CARTESIA_MODEL", "sonic-multilingual")
    elevenlabs_api_key: str = _ENV.get("ELEVENLABS_API_KEY", "")
    elevenlabs_voice_id: str = _ENV.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    # Configuración de Red y Transporte
    daily_room_url: str = _ENV.get("DAILY_ROOM_URL", "")
    daily_token: str = _ENV.get("DAILY_TOKEN", "")
    web_port: int = int(_ENV.get("WEB_PORT", 8765))
    web_host: str = _ENV.get("WEB_HOST", "0.0.0.0")

    def __init__(self, **kwargs):
        # Asignar valores base
        self.agent_name = _ENV.get("AGENT_NAME", "Aura")
        self.agent_language = _ENV.get("AGENT_LANGUAGE", "es")
        self.agent_system_prompt = _ENV.get("AGENT_SYSTEM_PROMPT", (
            "Eres Aura, una asistente e ingeniera de software de élite del proyecto pipecat-hexagonal-agent. "
            "Operas sobre una Arquitectura Hexagonal estricta estructurada en 'core/ports/' y 'adapters/', "
            "y cuentas con herramientas internas de Búsqueda Web en tiempo real y Runtime de Servidores MCP. "
            "\n\n[REGLAS ESTRICTAS DE AUTONOMÍA]:\n"
            "1. NUNCA le pidas al usuario que ejecute comandos en su terminal (como 'npm run...', 'ejecuta en terminal', 'revisa los logs en...'). "
            "2. Si el usuario te pide probar, sincronizar, crear o verificar una herramienta, EJECÚTALA tú misma mediante tus herramientas internas y entrega directamente los resultados de la acción ya ejecutada. "
            "3. Cuando se realice una acción en Google Calendar u otro MCP, confirma el evento, la hora y el resultado con entusiasmo y seguridad sin delegar tareas manuales. "
            "4. Responde siempre en español con concisión, tono natural y profesional para síntesis de voz fluida."
        ))
        self.stt_provider = STTProviderType(_ENV.get("STT_PROVIDER", STTProviderType.WHISPER_LOCAL.value))
        self.llm_provider = LLMProviderType(_ENV.get("LLM_PROVIDER", LLMProviderType.OLLAMA.value))
        self.tts_provider = TTSProviderType(_ENV.get("TTS_PROVIDER", TTSProviderType.PIPER_LOCAL.value))
        self.transport_provider = TransportProviderType(_ENV.get("TRANSPORT_PROVIDER", TransportProviderType.LOCAL_AUDIO.value))
        self.whisper_model_size = _ENV.get("WHISPER_MODEL_SIZE", "base")
        self.whisper_device = _ENV.get("WHISPER_DEVICE", "cpu")
        self.ollama_model = _ENV.get("OLLAMA_MODEL", "llama3.1:8b")
        self.ollama_base_url = _ENV.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        self.piper_voice_name = _ENV.get("PIPER_VOICE_NAME", "es_ES-davefx-medium")
        self.piper_model_path = _ENV.get("PIPER_MODEL_PATH", "")
        self.openai_api_key = _ENV.get("OPENAI_API_KEY", "")
        self.openai_model = _ENV.get("OPENAI_MODEL", "gpt-4o-mini")
        self.deepgram_api_key = _ENV.get("DEEPGRAM_API_KEY", "")
        self.deepgram_model = _ENV.get("DEEPGRAM_MODEL", "nova-2-general")
        self.cartesia_api_key = _ENV.get("CARTESIA_API_KEY", "")
        self.cartesia_voice_id = _ENV.get("CARTESIA_VOICE_ID", "79a125e8-cd45-4c13-8a67-188112f4dd22")
        self.cartesia_model = _ENV.get("CARTESIA_MODEL", "sonic-multilingual")
        self.elevenlabs_api_key = _ENV.get("ELEVENLABS_API_KEY", "")
        self.elevenlabs_voice_id = _ENV.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.daily_room_url = _ENV.get("DAILY_ROOM_URL", "")
        self.daily_token = _ENV.get("DAILY_TOKEN", "")
        self.web_port = int(_ENV.get("WEB_PORT", 8765))
        self.web_host = _ENV.get("WEB_HOST", "0.0.0.0")

        # Sobrescribir con argumentos kwargs
        for k, v in kwargs.items():
            key_lower = k.lower()
            if hasattr(self, key_lower):
                setattr(self, key_lower, v)


settings = AppSettings()
