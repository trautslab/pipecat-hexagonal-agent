import asyncio
from typing import Optional, Any
from config.logger_config import logger

from core.ports.stt_port import STTPort
from core.ports.llm_port import LLMPort
from core.ports.tts_port import TTSPort
from core.ports.transport_port import TransportPort
from core.domain.session import AgentSession

try:
    from pipecat.pipeline.pipeline import Pipeline
    from pipecat.pipeline.runner import PipelineRunner
    from pipecat.pipeline.task import PipelineTask, PipelineParams
    from pipecat.processors.aggregators.llm_response import (
        LLMAssistantResponseAggregator,
        LLMUserResponseAggregator,
    )
    from pipecat.frames.frames import TextFrame
except ImportError:
    class Pipeline:
        def __init__(self, processors):
            self.processors = processors

    class PipelineRunner:
        async def run(self, task):
            pass

    class PipelineTask:
        def __init__(self, pipeline, params=None):
            self.pipeline = pipeline
            self.params = params
        async def queue_frame(self, frame):
            pass

    class PipelineParams:
        def __init__(self, **kwargs):
            pass

    class LLMUserResponseAggregator:
        pass

    class LLMAssistantResponseAggregator:
        pass

    class TextFrame:
        def __init__(self, text):
            self.text = text


class VoiceAgentPipelineBuilder:
    """
    Orquestador del Dominio (Core).
    Ensambla y gestiona el ciclo de vida del agente Pipecat usando única y exclusivamente
    los puertos definidos por la arquitectura hexagonal.
    """

    def __init__(
        self,
        stt_port: STTPort,
        llm_port: LLMPort,
        tts_port: TTSPort,
        transport_port: TransportPort,
        session: AgentSession,
    ):
        self.stt = stt_port
        self.llm = llm_port
        self.tts = tts_port
        self.transport = transport_port
        self.session = session
        self.task: Optional[Any] = None
        self.runner: Optional[Any] = None

        logger.info(
            f"Inicializando Core Pipeline con puertos: "
            f"STT={self.stt.provider_name}, "
            f"LLM={self.llm.provider_name}, "
            f"TTS={self.tts.provider_name}, "
            f"Transport={self.transport.provider_name}"
        )

    def build_pipeline(self) -> Pipeline:
        """
        Ensambla el flujo de procesamiento de Pipecat con desacoplamiento total.
        """
        stt_service = self.stt.get_service()
        llm_service = self.llm.get_service()
        tts_service = self.tts.get_service()

        user_aggregator = LLMUserResponseAggregator()
        assistant_aggregator = LLMAssistantResponseAggregator()

        pipeline = Pipeline([
            self.transport.get_input(),   # 1. Entrada de Audio
            stt_service,                  # 2. Transcripción (Audio -> Texto)
            user_aggregator,              # 3. Agrupador de mensaje del usuario
            llm_service,                  # 4. Inferencia LLM (Texto -> Respuesta)
            tts_service,                  # 5. Síntesis (Respuesta -> Audio)
            self.transport.get_output(),  # 6. Salida de Audio al usuario
            assistant_aggregator          # 7. Registro de respuesta en historial
        ])

        return pipeline

    async def run(self, initial_greeting: Optional[str] = "¡Hola! ¿En qué puedo ayudarte hoy?"):
        """
        Ejecuta el agente y maneja la sesión conversacional.
        """
        pipeline = self.build_pipeline()
        
        self.task = PipelineTask(
            pipeline,
            params=PipelineParams(
                allow_interruptions=True,
                enable_metrics=True,
                send_initial_empty_metrics=False
            )
        )
        self.runner = PipelineRunner()

        logger.info("Pipeline construido exitosamente. Iniciando Runner...")

        if initial_greeting:
            async def send_greeting():
                await asyncio.sleep(1.0)
                if self.task:
                    logger.info(f"Enviando saludo inicial: '{initial_greeting}'")
                    await self.task.queue_frame(TextFrame(initial_greeting))

            asyncio.create_task(send_greeting())

        await self.runner.run(self.task)
