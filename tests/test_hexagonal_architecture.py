import unittest
import uuid
from config.settings import (
    AppSettings,
    STTProviderType,
    LLMProviderType,
    TTSProviderType,
    TransportProviderType,
)
from core.domain.session import AgentSession
from factories.agent_factory import AgentFactory
from adapters.mock_adapters import (
    MockSTTAdapter,
    MockLLMAdapter,
    MockTTSAdapter,
    MockTransportAdapter,
)
from adapters.transport.websocket_transport_adapter import WebSocketTransportAdapter
from core.services.pipeline_builder import VoiceAgentPipelineBuilder


class TestHexagonalArchitecture(unittest.TestCase):

    def test_agent_session_domain(self):
        """Valida la entidad de dominio AgentSession."""
        session = AgentSession(
            session_id=str(uuid.uuid4()),
            agent_name="TestBot",
            language="es",
            system_prompt="Eres un bot de prueba."
        )
        session.add_user_message("Hola")
        session.add_assistant_message("Hola, ¿cómo estás?")

        context = session.get_context_for_llm()
        self.assertEqual(len(context), 3)
        self.assertEqual(context[0]["role"], "system")
        self.assertEqual(context[1]["role"], "user")
        self.assertEqual(context[2]["role"], "assistant")

    def test_factory_with_mock_providers(self):
        """Valida la inyección de adaptadores mockeados a través de la factoría."""
        config = AppSettings(
            STT_PROVIDER=STTProviderType.MOCK,
            LLM_PROVIDER=LLMProviderType.MOCK,
            TTS_PROVIDER=TTSProviderType.MOCK,
            TRANSPORT_PROVIDER=TransportProviderType.LOCAL_AUDIO
        )

        agent_builder = AgentFactory.build_agent(config)
        self.assertIsInstance(agent_builder, VoiceAgentPipelineBuilder)
        self.assertEqual(agent_builder.stt.provider_name, "Mock STT (Simulación)")
        self.assertEqual(agent_builder.llm.provider_name, "Mock LLM (Simulación)")
        self.assertEqual(agent_builder.tts.provider_name, "Mock TTS (Simulación)")

    def test_factory_with_websocket_transport(self):
        """Valida la instanciación e inyección del adaptador WebSocketTransportAdapter."""
        config = AppSettings(
            STT_PROVIDER=STTProviderType.MOCK,
            LLM_PROVIDER=LLMProviderType.MOCK,
            TTS_PROVIDER=TTSProviderType.MOCK,
            TRANSPORT_PROVIDER=TransportProviderType.WEBSOCKET
        )
        agent_builder = AgentFactory.build_agent(config)
        self.assertIsInstance(agent_builder.transport, WebSocketTransportAdapter)
        self.assertEqual(agent_builder.transport.provider_name, "WebSocket Streaming (Web Client)")

    def test_pipeline_assembly_with_ports(self):
        """Valida que el Core Pipeline Builder ensamble la tubería de Pipecat correctamente."""
        stt = MockSTTAdapter()
        llm = MockLLMAdapter()
        tts = MockTTSAdapter()
        transport = MockTransportAdapter()
        session = AgentSession(
            session_id="test-123",
            agent_name="TestBot",
            language="es",
            system_prompt="Test"
        )

        builder = VoiceAgentPipelineBuilder(
            stt_port=stt,
            llm_port=llm,
            tts_port=tts,
            transport_port=transport,
            session=session
        )

        pipeline = builder.build_pipeline()
        self.assertIsNotNone(pipeline)
        self.assertTrue(len(pipeline.processors) >= 5)


if __name__ == "__main__":
    unittest.main()
