import uuid
from config.logger_config import logger

from config.settings import (
    AppSettings,
    settings,
    STTProviderType,
    LLMProviderType,
    TTSProviderType,
    TransportProviderType,
)
from core.domain.session import AgentSession
from core.ports.stt_port import STTPort
from core.ports.llm_port import LLMPort
from core.ports.tts_port import TTSPort
from core.ports.transport_port import TransportPort
from core.services.pipeline_builder import VoiceAgentPipelineBuilder

# Adaptadores
from adapters.stt.whisper_local_adapter import WhisperLocalSTTAdapter
from adapters.stt.deepgram_adapter import DeepgramSTTAdapter
from adapters.llm.ollama_adapter import OllamaLLMAdapter
from adapters.llm.openai_adapter import OpenAILLMAdapter
from adapters.tts.piper_adapter import PiperLocalTTSAdapter
from adapters.tts.cartesia_adapter import CartesiaTTSAdapter
from adapters.transport.local_audio_adapter import LocalAudioTransportAdapter
from adapters.transport.daily_webrtc_adapter import DailyWebRTCTransportAdapter
from adapters.transport.websocket_transport_adapter import WebSocketTransportAdapter
from adapters.mock_adapters import (
    MockSTTAdapter,
    MockLLMAdapter,
    MockTTSAdapter,
    MockTransportAdapter,
)


class AgentFactory:
    """
    Factory e Inyector de Dependencias.
    Resuelve e instancia los adaptadores concretos según la configuración,
    cumpliendo los puertos requeridos por el núcleo (Arquitectura Hexagonal).
    """

    @classmethod
    def create_stt_adapter(cls, config: AppSettings) -> STTPort:
        match config.stt_provider:
            case STTProviderType.WHISPER_LOCAL:
                return WhisperLocalSTTAdapter(
                    model_size=config.whisper_model_size,
                    device=config.whisper_device
                )
            case STTProviderType.DEEPGRAM:
                return DeepgramSTTAdapter(
                    api_key=config.deepgram_api_key or "",
                    language=config.agent_language
                )
            case STTProviderType.MOCK:
                return MockSTTAdapter()
            case _:
                raise ValueError(f"Proveedor STT no soportado: {config.stt_provider}")

    @classmethod
    def create_llm_adapter(cls, config: AppSettings) -> LLMPort:
        match config.llm_provider:
            case LLMProviderType.OLLAMA:
                return OllamaLLMAdapter(
                    base_url=config.ollama_base_url,
                    model=config.ollama_model,
                    system_prompt=config.agent_system_prompt
                )
            case LLMProviderType.OPENAI:
                return OpenAILLMAdapter(
                    api_key=config.openai_api_key or "",
                    model=config.openai_model,
                    system_prompt=config.agent_system_prompt
                )
            case LLMProviderType.MOCK:
                return MockLLMAdapter(system_prompt=config.agent_system_prompt)
            case _:
                raise ValueError(f"Proveedor LLM no soportado: {config.llm_provider}")

    @classmethod
    def create_tts_adapter(cls, config: AppSettings) -> TTSPort:
        match config.tts_provider:
            case TTSProviderType.PIPER_LOCAL:
                return PiperLocalTTSAdapter(
                    voice_name=config.piper_voice_name,
                    model_path=config.piper_model_path
                )
            case TTSProviderType.CARTESIA:
                return CartesiaTTSAdapter(
                    api_key=config.cartesia_api_key or "",
                    voice_id=config.cartesia_voice_id or ""
                )
            case TTSProviderType.MOCK:
                return MockTTSAdapter()
            case _:
                raise ValueError(f"Proveedor TTS no soportado: {config.tts_provider}")

    @classmethod
    def create_transport_adapter(cls, config: AppSettings) -> TransportPort:
        match config.transport_provider:
            case TransportProviderType.LOCAL_AUDIO:
                return LocalAudioTransportAdapter()
            case TransportProviderType.DAILY_WEBRTC:
                return DailyWebRTCTransportAdapter(
                    room_url=config.daily_room_url or "",
                    token=config.daily_token,
                    bot_name=config.agent_name
                )
            case TransportProviderType.WEBSOCKET:
                return WebSocketTransportAdapter()
            case _:
                return MockTransportAdapter()

    @classmethod
    def build_agent(
        cls,
        custom_config: AppSettings = settings
    ) -> VoiceAgentPipelineBuilder:
        """
        Construye la instancia completa del agente inyectando los adaptadores en el Core.
        """
        session = AgentSession(
            session_id=str(uuid.uuid4()),
            agent_name=custom_config.agent_name,
            language=custom_config.agent_language,
            system_prompt=custom_config.agent_system_prompt
        )

        stt_adapter = cls.create_stt_adapter(custom_config)
        llm_adapter = cls.create_llm_adapter(custom_config)
        tts_adapter = cls.create_tts_adapter(custom_config)
        transport_adapter = cls.create_transport_adapter(custom_config)

        logger.info(
            f"Ensamblando Agente de Voz '{custom_config.agent_name}' con arquitectura hexagonal..."
        )

        return VoiceAgentPipelineBuilder(
            stt_port=stt_adapter,
            llm_port=llm_adapter,
            tts_port=tts_adapter,
            transport_port=transport_adapter,
            session=session
        )
