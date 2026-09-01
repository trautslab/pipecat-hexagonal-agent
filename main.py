import asyncio
from config.logger_config import logger
from config.settings import settings
from factories.agent_factory import AgentFactory


async def main():
    logger.info("=" * 60)
    logger.info("🤖 INICIANDO AGENTE DE VOZ PIPECAT (ARQUITECTURA HEXAGONAL)")
    logger.info("=" * 60)
    logger.info(f"• Nombre del Agente: {settings.agent_name}")
    logger.info(f"• Proveedor STT:     {settings.stt_provider}")
    logger.info(f"• Proveedor LLM:     {settings.llm_provider}")
    logger.info(f"• Proveedor TTS:     {settings.tts_provider}")
    logger.info(f"• Transporte:        {settings.transport_provider}")
    logger.info("=" * 60)

    try:
        # Construcción del agente mediante Factory e Inyección de Dependencias
        agent = AgentFactory.build_agent(settings)
        
        # Ejecutar Pipeline
        await agent.run(
            initial_greeting="¡Hola! Soy tu asistente de voz. ¿De qué te gustaría hablar hoy?"
        )
    except KeyboardInterrupt:
        logger.warning("\nSesión finalizada por el usuario.")
    except Exception as e:
        logger.error(f"Error en la ejecución del agente: {e}")


if __name__ == "__main__":
    asyncio.run(main())
