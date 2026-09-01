#!/usr/bin/env python3
"""
Automated Eval Harness (AI-SDLC Standard)
Ejecuta bucles de evaluación deterministas para contratos de tareas agénticas.
"""
import sys
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

        # Validar existencia de archivos del cliente web
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


def main():
    parser = argparse.ArgumentParser(description="AI-SDLC Eval Harness")
    parser.add_argument("--task", default=None, help="ID de la tarea a evaluar (e.g. TASK-001, TASK-002, TASK-003, TASK-004)")
    parser.add_argument("--all", action="store_true", help="Evaluar todas las tareas registradas")

    args = parser.parse_args()

    results = {}

    if args.task == "TASK-001" or args.all or not args.task:
        res = eval_task_001_core_and_ports()
        results["TASK-001"] = res
        log_event("EVALUATION", "TASK-001", "SUCCESS" if res else "FAILED", "Eval Harness executed")

    if args.task == "TASK-002" or args.all or not args.task:
        res = eval_task_002_zero_cost_local_stack()
        results["TASK-002"] = res
        log_event("EVALUATION", "TASK-002", "SUCCESS" if res else "FAILED", "Eval Harness executed")

    if args.task == "TASK-003" or args.all or not args.task:
        res = eval_task_003_cloud_adapters()
        results["TASK-003"] = res
        log_event("EVALUATION", "TASK-003", "SUCCESS" if res else "FAILED", "Eval Harness executed")

    if args.task == "TASK-004" or args.all or not args.task:
        res = eval_task_004_websocket_transport_and_web_ui()
        results["TASK-004"] = res
        log_event("EVALUATION", "TASK-004", "SUCCESS" if res else "FAILED", "Eval Harness executed")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n📈 [RESUMEN EVALUATION HARNESS] {passed}/{total} tareas superadas.")

    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
