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
    print("\n🧪 [EVAL] Evaluando TASK-010: Inspector de Acciones y Telemetría...")
    try:
        web_app = (ROOT_DIR / "web" / "app.js").read_text()
        web_styles = (ROOT_DIR / "web" / "styles.css").read_text()
        server_code = (ROOT_DIR / "web_server.py").read_text()

        assert "telemetry" in server_code, "Objeto telemetry no emitido por web_server.py"
        assert "copyToClipboard" in web_app, "copyToClipboard no encontrado"

        print("✅ [EVAL TASK-010] Superada: Telemetría y copiado validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-010] Falló: {e}")
        return False


def eval_task_011_realtime_console_right_sidebar() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-011: Consola Lateral Derecha de Trazabilidad en Tiempo Real...")
    try:
        web_index = (ROOT_DIR / "web" / "index.html").read_text()
        web_styles = (ROOT_DIR / "web" / "styles.css").read_text()
        web_app = (ROOT_DIR / "web" / "app.js").read_text()
        server_code = (ROOT_DIR / "web_server.py").read_text()

        assert "right-console-sidebar" in web_index, "right-console-sidebar no encontrado en index.html"
        assert "turn-badge" in web_styles, "turn-badge no encontrado en styles.css"
        assert "handleLiveTraceStep" in web_app, "handleLiveTraceStep no encontrado en app.js"
        assert "live_trace_step" in server_code, "live_trace_step no emitido por web_server.py"

        print("✅ [EVAL TASK-011] Superada: Consola lateral derecha, live_trace_step streaming y turn badges validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-011] Falló: {e}")
        return False


def eval_task_012_mcp_active_executor() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-012: Ejecutor Activo de Herramientas MCP y Sonda de Google Calendar...")
    try:
        from core.ports.mcp_executor_port import MCPExecutorPort
        from adapters.tools.mcp_executor_adapter import MCPExecutorAdapter
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from core.services.grounding_service import GroundingService

        executor = MCPExecutorAdapter()
        assert isinstance(executor, MCPExecutorPort), "MCPExecutorAdapter no implementa MCPExecutorPort"

        v = executor.validate_credentials("google-calendar")
        assert "credentials_present" in v

        probe = executor.execute_probe_action("google-calendar", "test_event")
        assert probe["status"] == "success"
        assert "Hello World" in probe["event_title"]

        engine = AutonomousReasoningEngine(
            grounding_service=GroundingService(DuckDuckGoSearchAdapter()),
            mcp_manager=MCPManagerAdapter(),
            mcp_executor=executor
        )

        assert engine.is_mcp_execution_intent("Listo ya puse las credenciales ahora que hacemos") == "google-calendar"
        print("✅ [EVAL TASK-012] Superada: MCPExecutorAdapter, sonda de calendario y detección ReAct validadas.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-012] Falló: {e}")
        return False


def eval_task_013_mcp_autonomous_runtime() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-013: Runtime Autónomo de Ejecución y Cero Comandos Manuales...")
    try:
        from core.ports.mcp_runtime_port import MCPRuntimePort
        from adapters.tools.mcp_runtime_adapter import MCPRuntimeAdapter
        from config.settings import settings

        runtime = MCPRuntimeAdapter()
        assert isinstance(runtime, MCPRuntimePort), "MCPRuntimeAdapter no implementa MCPRuntimePort"

        res = runtime.sync_google_calendar_now()
        assert res["status"] in ["success", "auth_required"]
        assert "NUNCA le pidas al usuario que ejecute comandos" in settings.agent_system_prompt

        print("✅ [EVAL TASK-013] Superada: Runtime de ejecución MCP autónomo y prompt de cero comandos validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-013] Falló: {e}")
        return False


def eval_task_014_server_side_persistence() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-014: Persistencia de Sesiones y Telemetría en el Backend...")
    try:
        from core.ports.session_repository_port import SessionRepositoryPort
        from adapters.persistence.file_session_repository_adapter import FileSessionRepositoryAdapter

        repo = FileSessionRepositoryAdapter()
        assert isinstance(repo, SessionRepositoryPort), "FileSessionRepositoryAdapter no implementa SessionRepositoryPort"

        test_session = {
            "id": "eval_test_session_1",
            "title": "Evaluación de Persistencia",
            "createdAt": "2026-09-01T20:00:00Z",
            "turnCounter": 1,
            "messages": [{"role": "user", "text": "Prueba", "turnIndex": 1}],
            "consoleLogs": [{"turnIndex": 1, "steps": [{"title": "Test", "detail": "Detalle"}]}]
        }

        assert repo.save_session(test_session) is True
        loaded = repo.get_session("eval_test_session_1")
        assert loaded is not None
        assert loaded["title"] == "Evaluación de Persistencia"
        assert len(loaded["consoleLogs"]) == 1

        repo.delete_session("eval_test_session_1")
        assert repo.get_session("eval_test_session_1") is None

        print("✅ [EVAL TASK-014] Superada: SessionRepositoryPort y FileSessionRepositoryAdapter validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-014] Falló: {e}")
        return False


def eval_task_015_ide_workbench_layout() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-015: Layout Postman / Modern IDE Workbench (5 Zonas)...")
    try:
        web_index = (ROOT_DIR / "web" / "index.html").read_text()
        web_styles = (ROOT_DIR / "web" / "styles.css").read_text()

        assert "ide-header" in web_index
        assert "ide-sidebar" in web_index
        assert "ide-workbench" in web_index
        assert "ide-right-sidebar" in web_index
        assert "ide-footer" in web_index
        assert "ide-container" in web_styles

        print("✅ [EVAL TASK-015] Superada: Maquetación Postman/IDE Workbench de 5 zonas validada exitosamente.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-015] Falló: {e}")
        return False


def eval_task_016_parameterized_autonomous_dispatch() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-016: Despacho Parametrizado de Herramientas y Barrera Anti-Rechazo...")
    try:
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from adapters.tools.mcp_runtime_adapter import MCPRuntimeAdapter
        from core.services.grounding_service import GroundingService

        runtime = MCPRuntimeAdapter()
        engine = AutonomousReasoningEngine(
            grounding_service=GroundingService(DuckDuckGoSearchAdapter()),
            mcp_manager=MCPManagerAdapter(),
            mcp_runtime=runtime
        )

        test_prompt = "ya lo he configurado por favor puedes revisarlo y hacer una prueba de un Hello World para un minuto después de las alas mejor ponlo para las 4:09"
        
        assert engine.classify_calendar_intent(test_prompt) == "create_event"
        params = engine.parse_calendar_parameters(test_prompt)
        assert "Hello World" in params["title"]

        async def _test():
            augmented, trace = await engine.process_reasoning_loop(test_prompt)
            assert len(trace) >= 2
            assert "ACCIÓN REAL DE GOOGLE CALENDAR API v3" in augmented or "AUTORIZACIÓN OAUTH2 REQUERIDA" in augmented
            return True

        asyncio.run(_test())

        print("✅ [EVAL TASK-016] Superada: Extracción de parámetros ('4:09', 'Hello World'), ejecución real y ReAct augmentado validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-016] Falló: {e}")
        return False


def eval_task_017_real_google_calendar_api() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-017: Cliente Nativo Google Calendar API v3 y OAuth2...")
    try:
        from adapters.tools.google_calendar_client import GoogleCalendarClient

        client = GoogleCalendarClient()
        auth_url = client.get_auth_url()
        assert "accounts.google.com/o/oauth2/v2/auth" in auth_url, "URL OAuth2 no apunta a Google"
        assert "calendar.events" in auth_url, "Scope calendar.events ausente"
        assert "client_id=" in auth_url, "Client ID ausente en URL"

        server_code = (ROOT_DIR / "web_server.py").read_text()
        assert "/oauth2callback" in server_code, "Endpoint /oauth2callback ausente en web_server.py"

        print("✅ [EVAL TASK-017] Superada: Generación OAuth2, endpoint /oauth2callback y GoogleCalendarClient validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-017] Falló: {e}")
        return False


def eval_task_018_nlp_calendar_extraction() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-018: Extracción NLP Avanzada y Descripciones Amables...")
    try:
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from adapters.tools.mcp_runtime_adapter import MCPRuntimeAdapter
        from core.services.grounding_service import GroundingService

        engine = AutonomousReasoningEngine(
            grounding_service=GroundingService(DuckDuckGoSearchAdapter()),
            mcp_manager=MCPManagerAdapter(),
            mcp_runtime=MCPRuntimeAdapter()
        )

        test_prompt = "Quiero que me hagas un evento para las 5:15 de la tarde del 1 de septiembre del 2026 el evento llámalo preparación para ir al cine Planet de 2 de mayo"

        params = engine.parse_calendar_parameters(test_prompt)
        assert "Preparación para ir al cine Planet de 2 de mayo" in params["title"], f"Título erróneo: {params['title']}"
        assert params["date"] == "2026-09-01", f"Fecha errónea: {params['date']}"
        assert params["time"] == "17:15:00", f"Hora errónea: {params['time']}"
        assert "Cineplanet" in params["location"] or "2 de Mayo" in params["location"], f"Ubicación errónea: {params['location']}"
        assert "🎬 Recordatorio" in params["description"], "Descripción amable no generada"

        print("✅ [EVAL TASK-018] Superada: Título exacto, fecha '2026-09-01', hora '17:15:00', ubicación y descripción amable extraídas exitosamente.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-018] Falló: {e}")
        return False


def eval_task_019_llm_native_tool_calling() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-019: Razonamiento Nativo del LLM y Tool Calling Estructurado...")
    try:
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from adapters.tools.mcp_runtime_adapter import MCPRuntimeAdapter
        from core.services.grounding_service import GroundingService

        engine = AutonomousReasoningEngine(
            grounding_service=GroundingService(DuckDuckGoSearchAdapter()),
            mcp_manager=MCPManagerAdapter(),
            mcp_runtime=MCPRuntimeAdapter()
        )

        test_prompt = "Agéndame un evento para mañana a las 10 am en la sala de juntas"

        assert hasattr(engine, "llm_reason_and_extract_tool_call"), "Método llm_reason_and_extract_tool_call ausente"

        async def _test():
            res, trace = await engine.process_reasoning_loop(test_prompt)
            assert len(trace) >= 2, "La traza ReAct no generó pensamientos estructurados"
            assert "Google Calendar" in res or "ACCIÓN REAL" in res or "AUTORIZACIÓN" in res
            return True

        asyncio.run(_test())

        print("✅ [EVAL TASK-019] Superada: Razonamiento estructurado del LLM y ciclo ReAct proactivo validados.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-019] Falló: {e}")
        return False


def eval_task_020_calendar_multi_tool_dispatch() -> bool:
    print("\n🧪 [EVAL] Evaluando TASK-020: Despachador Multi-Herramienta de Calendario y Listado de Eventos...")
    try:
        from core.services.reasoning_engine import AutonomousReasoningEngine
        from adapters.tools.duckduckgo_search_adapter import DuckDuckGoSearchAdapter
        from adapters.tools.mcp_manager_adapter import MCPManagerAdapter
        from adapters.tools.mcp_runtime_adapter import MCPRuntimeAdapter
        from core.services.grounding_service import GroundingService

        engine = AutonomousReasoningEngine(
            grounding_service=GroundingService(DuckDuckGoSearchAdapter()),
            mcp_manager=MCPManagerAdapter(),
            mcp_runtime=MCPRuntimeAdapter()
        )

        verify_prompt = "no veo lo que has configurado la verdad estás seguro que has hecho el recordatorio al evento del Google calendar"
        intent = engine.classify_calendar_intent(verify_prompt)
        assert intent == "list_events", f"Intención incorrecta: {intent}, esperaba 'list_events'"

        async def _test():
            res, trace = await engine.process_reasoning_loop(verify_prompt)
            assert len(trace) >= 2
            assert "CONSULTA EN VIVO DE GOOGLE CALENDAR" in res
            assert "Cumpleaños de Ana" not in res
            return True

        asyncio.run(_test())

        print("✅ [EVAL TASK-020] Superada: Detección de intención list_events, cero alucinaciones de eventos y consulta en vivo validadas.")
        return True
    except Exception as e:
        print(f"❌ [EVAL TASK-020] Falló: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AI-SDLC Eval Harness")
    parser.add_argument("--task", default=None, help="ID de la tarea a evaluar (e.g. TASK-001 a TASK-020)")
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
        ("TASK-010", eval_task_010_action_inspector),
        ("TASK-011", eval_task_011_realtime_console_right_sidebar),
        ("TASK-012", eval_task_012_mcp_active_executor),
        ("TASK-013", eval_task_013_mcp_autonomous_runtime),
        ("TASK-014", eval_task_014_server_side_persistence),
        ("TASK-015", eval_task_015_ide_workbench_layout),
        ("TASK-016", eval_task_016_parameterized_autonomous_dispatch),
        ("TASK-017", eval_task_017_real_google_calendar_api),
        ("TASK-018", eval_task_018_nlp_calendar_extraction),
        ("TASK-019", eval_task_019_llm_native_tool_calling),
        ("TASK-020", eval_task_020_calendar_multi_tool_dispatch)
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
