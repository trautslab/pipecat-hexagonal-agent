from typing import Optional
from config.logger_config import logger
from core.ports.search_port import SearchPort


class GroundingService:
    """
    Servicio de Dominio para Grounding y Búsqueda Web Factual.
    Invocado exclusivamente cuando el Enrutador Cognitivo LLM decide ejecutar la herramienta 'web_search'.
    """

    def __init__(self, search_port: SearchPort):
        self.search_port = search_port

    async def search_and_augment(self, query: str, original_prompt: str) -> str:
        """
        Ejecuta la búsqueda web en tiempo real y construye el prompt con evidencias factuales.
        """
        logger.info(f"🔎 [Grounding] Búsqueda factual solicitada por el LLM: '{query}'")
        evidence = await self.search_port.search(query)

        augmented_prompt = (
            f"[INFORMACIÓN VERIFICADA DESDE INTERNET EN TIEMPO REAL]:\n"
            f"{evidence}\n\n"
            f"[CONSULTA DEL USUARIO]:\n"
            f"{original_prompt}\n\n"
            f"[INSTRUCCIÓN CRÍTICA]: Responde a la pregunta del usuario basándote ESTRICTAMENTE en la información verificada anterior. "
            f"Di los datos exactos sin inventar. Responde en español de forma breve y conversacional."
        )

        return augmented_prompt
