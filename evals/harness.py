#!/usr/bin/env python3
"""
Automated Eval Harness (AI-SDLC Standard)
Ejecuta bucles de evaluación deterministas para contratos de tareas agénticas.
"""
import sys
import asyncio
import argparse
from pathlib import Path

# Añadir raíz al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.telemetry_logger import log_event
from config.settings import AppSettings, STTProviderType, LLMProviderType, TTSProviderType, TransportProviderType
from factories.agent_factory import AgentFactory
from core.services.pipeline_builder import VoiceAgentPipelineBuilder
from core.domain.session import AgentSession


def eval_task_001_core_and_ports() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-001: Núcleo y Puertos de Arquitectura Hexagonal...")
    try:
        from core.ports.stt_port import STTPort
        from core.ports.llm_port import LLMPort
        from core.ports.tts_port import TTSPort
        from core.ports.transport_port import TransportPort

        from adapters.mock_adapters import MockSTTAdapter, MockLLMAdapter, MockTTSAdapter, MockTransportAdapter
        
        session = AgentSession("session-1", "TestBot", "es", "System Prompt")
        builder = VoiceAgentPipelineBuilder(
            stt_port=MockSTTAdapter(),
            llm_port=MockLLMAdapter(),
            tts_port=MockTTSAdapter(),
            transport_port=MockTransportAdapter(),
            session=session
        )
        pipeline = builder.build_pipeline()
        assert pipeline is not None, "El pipeline generado es None"
        assert len(pipeline.processors) >= 5, "El pipeline no contiene la cantidad esperada de procesadores"
        print("✅ [EVAL TASK-001] Superada: Contratos y pipeline orquestados exitosamente.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-001] Falló: {e}")
        return False


def eval_task_002_zero_cost_local_stack() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-002: Pila 100% Gratuita y Local (Ollama + Whisper + Piper)...")
    try:
        config = AppSettings(
            STT_PROVIDER=STTProviderType.WHISPER_LOCAL,
            LLM_PROVIDER=LLMProviderType.OLLAMA,
            TTS_PROVIDER=TTSProviderType.PIPER_LOCAL,
            TRANSPORT_PROVIDER=TransportProviderType.LOCAL_AUDIO
        )
        builder = AgentFactory.build_agent(config)
        assert "WhisperLocal" in builder.stt.provider_name
        assert "Ollama Local" in builder.llm.provider_name
        assert "PiperTTS Local" in builder.tts.provider_name
        assert "Local Audio" in builder.transport.provider_name
        print("✅ [EVAL TASK-002] Superada: Adaptadores locales resueltos e inyectados sin costo.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-002] Falló: {e}")
        return False


def eval_task_003_cloud_adapters() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-003: Adaptadores Cloud e Híbridos...")
    try:
        config = AppSettings(
            STT_PROVIDER=STTProviderType.DEEPGRAM,
            LLM_PROVIDER=LLMProviderType.OPENAI,
            TTS_PROVIDER=TTSProviderType.CARTESIA,
            TRANSPORT_PROVIDER=TransportProviderType.DAILY_WEBRTC,
            OPENAI_API_KEY="sk-dummy",
            DEEPGRAM_API_KEY="dg-dummy",
            CARTESIA_API_KEY="cart-dummy",
            DAILY_ROOM_URL="https://demo.daily.co/test"
        )
        builder = AgentFactory.build_agent(config)
        assert "Deepgram" in builder.stt.provider_name
        assert "OpenAI" in builder.llm.provider_name
        assert "Cartesia" in builder.tts.provider_name
        assert "Daily WebRTC" in builder.transport.provider_name
        print("✅ [EVAL TASK-003] Superada: Conmutación Cloud resuelta correctamente.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-003] Falló: {e}")
        return False


def eval_task_004_websocket_transport_and_web_ui() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-004: Interfaz Web y Adaptador WebSocket...")
    try:
        from adapters.transport.websocket_transport_adapter import WebSocketTransportAdapter
        config = AppSettings(
            STT_PROVIDER=STTProviderType.MOCK,
            LLM_PROVIDER=LLMProviderType.MOCK,
            TTS_PROVIDER=TTSProviderType.MOCK,
            TRANSPORT_PROVIDER=TransportProviderType.WEBSOCKET
        )
        builder = AgentFactory.build_agent(config)
        assert "WebSocket Streaming" in builder.transport.provider_name
        assert isinstance(builder.transport, WebSocketTransportAdapter)

        web_index = ROOT_DIR / "web" / "index.html"
        web_styles = ROOT_DIR / "web" / "styles.css"
        web_app = ROOT_DIR / "web" / "app.js"
        assert web_index.exists(), "web/index.html no existe"
        assert web_styles.exists(), "web/styles.css no existe"
        assert web_app.exists(), "web/app.js no existe"

        print("✅ [EVAL TASK-004] Superada: Adaptador WebSocket y Frontend Web validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-004] Falló: {e}")
        return False


def eval_task_005_web_search_grounding() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-005: Herramienta de Búsqueda Web y Grounding Factual...")
    try:
        from core.ports.search_port import SearchPort
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from core.services.grounding_service import GroundingService

        search_adapter = DuckDuckGoSearchAdapter()
        assert isinstance(search_adapter, SearchPort), "El adaptador no implementa SearchPort"

        grounding = GroundingService(search_adapter)
        assert grounding.should_search("¿Dónde queda la Universidad Nacional de Ingeniería?") is True
        assert grounding.should_search("Hola") is False

        async def _test():
            prompt = await grounding.get_grounded_prompt("Universidad Nacional de Ingenieria del Peru")
            assert "[INFORMACIÓN VERIFICADA" in prompt
            return True

        asyncio.run(_test())
        print("✅ [EVAL TASK-005] Superada: SearchPort, DuckDuckGo adapter y GroundingService validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-005] Falló: {e}")
        return False


def eval_task_006_chat_history_and_copy() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-006: Historial de Conversaciones y Acciones de Copiado...")
    try:
        web_index = (ROOT_DIR / "web" / "index.html").read_text()
        web_app = (ROOT_DIR / "web" / "app.js").read_text()

        assert "sidebar" in web_index, "Sidebar no encontrado en index.html"
        assert "history-list" in web_index, "history-list no encontrado en index.html"
        assert "copyToClipboard" in web_app, "copyToClipboard no implementado en app.js"

        print("✅ [EVAL TASK-006] Superada: Sidebar de chats, persistencia y botones de copiado validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-006] Falló: {e}")
        return False


def eval_task_007_mcp_proactive_scaffolding() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-007: Autoconocimiento del Sistema y Scaffolding Proactivo de MCPs...")
    try:
        from config.settings import settings
        prompt = settings.agent_system_prompt
        assert "pipecat-hexagonal-agent" in prompt, "System prompt no conoce el repositorio"
        assert "core/ports/" in prompt, "System prompt no conoce la capa de puertos"
        assert "adapters/" in prompt, "System prompt no conoce la capa de adaptadores"

        print("✅ [EVAL TASK-007] Superada: Identidad proactiva y autoconocimiento de arquitectura validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-007] Falló: {e}")
        return False


def eval_task_008_react_reasoning_engine() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-008: Motor de Razonamiento Autónomo ReAct (OpenClaw)...")
    try:
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from core.services.grounding_service import GroundingService

        s_adapter = DuckDuckGoSearchAdapter()
        m_adapter = MCPManagerAdapter()
        g_service = GroundingService(s_adapter)
        engine = AutonomousReasoningEngine(g_service, m_adapter)

        async def _test():
            p, trace = await engine.process_reasoning_loop("Quisiera instalar Google Calendar")
            assert len(trace) >= 2, "La traza de razonamiento no emitió pensamientos"
            assert "ACCIÓN AUTÓNOMA" in p or "mcp-servers.json" in p
            return True

        asyncio.run(_test())
        print("✅ [EVAL TASK-008] Superada: Ciclo ReAct de razonamiento y emisión de pensamientos validado.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-008] Falló: {e}")
        return False


def eval_task_009_dynamic_mcp_manager() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-009: Gestor Dinámico de Servidores MCP...")
    try:
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        mcp_adapter = MCPManagerAdapter()
        assert mcp_adapter.is_mcp_intent("Instala el MCP de Google Calendar") == "google-calendar"
        assert mcp_adapter.is_mcp_intent("Hola") is None

        res = mcp_adapter.install_or_configure_mcp("google-calendar")
        assert res["status"] == "success"
        assert "GOOGLE_CALENDAR_CLIENT_ID" in res["required_env_vars"]

        print("✅ [EVAL TASK-009] Superada: MCPManagerAdapter configuró el servidor y .env con éxito.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-009] Falló: {e}")
        return False


def eval_task_010_action_inspector() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-010: Inspector Desplegable de Acciones y Telemetría...")
    try:
        web_app = (ROOT_DIR / "web" / "app.js").read_text()
        web_styles = (ROOT_DIR / "web" / "styles.css").read_text()
        server_code = (ROOT_DIR / "web_server.py").read_text()

        assert "action-inspector" in web_styles, "Estilos de action-inspector no encontrados"
        assert "copyTelemetryToClipboard" in web_app, "Método copyTelemetryToClipboard no encontrado en app.js"
        assert "telemetry" in server_code, "Objeto telemetry no emitido por web_server.py"

        print("✅ [EVAL TASK-010] Superada: Desplegable ActionInspector y botón de copiado de telemetría validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-010] Falló: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AI-SDLC Eval Harness")
    parser.add_argument("--task", default=None, help="ID de la tarea a evaluar (e.g. TASK-001 a TASK-010)")
    parser.add_argument("--all", action="store_true", help="Evaluar todas las tareas registradas")

    args = parser.parse_args()

    results = {}

    tasks = [
        ("TASK-001", eval_task_001_core_and_ports),
        ("TASK-002", eval_task_002_zero_cost_local_stack),
        ("TASK-003", eval_task_003_cloud_adapters),
        ("TASK-004", eval_task_004_websocket_transport_and_web_ui),
        ("TASK-005", eval_task_005_web_search_grounding),
        ("TASK-006", eval_task_006_chat_history_and_copy),
        ("TASK-007", eval_task_007_mcp_proactive_scaffolding),
        ("TASK-008", eval_task_008_react_reasoning_engine),
        ("TASK-009", eval_task_009_dynamic_mcp_manager),
        ("TASK-010", eval_task_010_action_inspector)
    ]

    for task_id, fn in tasks:
        if args.task == task_id or args.all or not args.task:
            res = fn()
            results[task_id] = res
            log_event("EVALUATION", task_id, "SUCCESS" if res else "FAILED", "Eval Harness executed")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n📈 [RESUMEN EVALUATION HARNESS] {passed}/{total} tareas superadas.")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
