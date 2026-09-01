import re
from typing import Optional
from config.logger_config import logger
from core.ports.search_port import SearchPort


class GroundingService:
    """
    Servicio de Dominio para Grounding y Anti-Alucinación.
    Orquesta la búsqueda web en tiempo real y compone prompts enriquecidos con evidencias.
    """

    def __init__(self, search_port: SearchPort):
        self.search_port = search_port

    def should_search(self, user_text: str) -> bool:
        """Determina si la consulta contiene intenciones factuales, geográficas o de información."""
        text_lower = user_text.lower().strip()

        # Preguntas cortas de saludo o cortesía no necesitan búsqueda
        if text_lower in ["hola", "buenos días", "buenas tardes", "cómo estás", "gracias", "adiós", "chao"]:
            return False

        # Patrones que denotan consultas factuales
        patterns = [
            r"\bd[oó]nde\b",
            r"\bqui[eé]n\b",
            r"\bcu[aá]ndo\b",
            r"\bqu[eé] es\b",
            r"\bc[oó]mo llegar\b",
            r"\buniversidad\b",
            r"\bcolegio\b",
            r"\bdirecci[oó]n\b",
            r"\bubicaci[oó]n\b",
            r"\bdistrito\b",
            r"\bavenida\b",
            r"\bprecio\b",
            r"\bnoticia\b",
            r"\bper[uú]\b",
            r"\blima\b"
        ]

        for p in patterns:
            if re.search(p, text_lower):
                return True
        return len(user_text.split()) >= 4

    async def get_grounded_prompt(self, user_prompt: str) -> str:
        """
        Ejecuta la búsqueda y construye el prompt con evidencias reales para el LLM.
        """
        if not self.should_search(user_prompt):
            return user_prompt

        logger.info(f"🔎 [Grounding] Pregunta factual detectada: '{user_prompt}'")
        evidence = await self.search_port.search(user_prompt)

        augmented_prompt = (
            f"[INFORMACIÓN VERIFICADA DESDE INTERNET EN TIEMPO REAL]:\n"
            f"{evidence}\n\n"
            f"[PREGUNTA DEL USUARIO]:\n"
            f"{user_prompt}\n\n"
            f"[INSTRUCCIÓN CRÍTICA]: Responde a la pregunta del usuario basándote ESTRICTAMENTE en la información verificada anterior. "
            f"Di los datos exactos (dirección, distrito, avenidas, hechos) sin inventar. Responde en español de forma breve y conversacional."
        )

        return augmented_prompt
