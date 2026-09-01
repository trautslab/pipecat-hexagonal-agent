import re
from typing import Optional
from config.logger_config import logger
from core.ports.search_port import SearchPort


class GroundingService:
    """
    Servicio de Dominio para Grounding y Anti-Alucinación.
    Orquesta la búsqueda web en tiempo real y compone prompts enriquecidos con evidencias.
    Aísla las solicitudes de calendario y recordatorios personales para evitar búsquedas web espurias.
    """

    def __init__(self, search_port: SearchPort):
        self.search_port = search_port

    def should_search(self, user_text: str) -> bool:
        """Determina si la consulta contiene intenciones factuales, geográficas o de información web."""
        text_lower = user_text.lower().strip()

        # 1. No buscar si es un saludo, cortesía o despedida
        if text_lower in ["hola", "buenos días", "buenas tardes", "cómo estás", "gracias", "adiós", "chao"]:
            return False

        # 2. Aislamiento estricto: Si el usuario está pidiendo un recordatorio o acción de calendario, NUNCA buscar en web
        calendar_and_reminder_terms = [
            "recordar", "recuérdame", "recuerdame", "recordatorio", "avísame", "avisame",
            "agenda", "agéndame", "agendame", "agendes", "agendar", "evento", "cita", "reunión",
            "reunion", "calendar", "calendario", "descongelar", "pollo", "cine", "cineplanet",
            "mcp", "configur", "credenciales", "token", "google"
        ]
        if any(term in text_lower for term in calendar_and_reminder_terms):
            return False

        # 3. Patrones explícitos que denotan consultas factuales de conocimiento o internet
        factual_patterns = [
            r"\bbusca\s+(?:en\s+internet|en\s+la\s+web|informaci[oó]n|noticias)\b",
            r"\binvestiga\b",
            r"\bd[oó]nde\s+queda\b",
            r"\bqui[eé]n\s+es\b",
            r"\bqu[eé]\s+es\s+[a-zA-Záéíóúñ]{3,}\b",
            r"\bc[oó]mo\s+llegar\s+a\b",
            r"\buniversidad\s+nacional\b",
            r"\bprecio\s+del?\b",
            r"\bnoticias\s+de\b",
            r"\bcapital\s+de\b",
            r"\bhistoria\s+de\b"
        ]

        for p in factual_patterns:
            if re.search(p, text_lower):
                return True

        return False

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
            f"[PREGUNTA DEL USUARIO]:\n{user_prompt}\n\n"
            f"[INSTRUCCIÓN CRÍTICA]: Responde a la pregunta del usuario basándote ESTRICTAMENTE en la información verificada anterior. "
            f"Di los datos exactos (dirección, distrito, avenidas, hechos) sin inventar. Responde en español de forma breve y conversacional."
        )

        return augmented_prompt
