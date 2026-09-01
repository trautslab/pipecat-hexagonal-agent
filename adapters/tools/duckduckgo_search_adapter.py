import asyncio
import json
import urllib.request
import urllib.parse
import re
from typing import List
from config.logger_config import logger
from core.ports.search_port import SearchPort


class DuckDuckGoSearchAdapter(SearchPort):
    """
    Adaptador de búsqueda web 100% gratuito y sin API keys.
    Combina DuckDuckGo y Wikipedia API para obtener evidencias factuales en vivo.
    """

    def __init__(self, timeout: float = 3.5):
        self.timeout = timeout

    async def search(self, query: str, max_results: int = 3) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._sync_search, query, max_results)

    def _sync_search(self, query: str, max_results: int) -> str:
        logger.info(f"🌐 [WebSearch] Buscando evidencias en internet para: '{query}'...")
        results = []

        # 1. Consulta enciclopédica vía Wikipedia API en español
        try:
            wiki_encoded = urllib.parse.quote(query)
            wiki_url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={wiki_encoded}&utf8=&format=json&srlimit={max_results}"
            req = urllib.request.Request(
                wiki_url,
                headers={"User-Agent": "AuraVoiceAgent/1.0 (https://github.com/trautslab/pipecat-hexagonal-agent)"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                search_items = data.get("query", {}).get("search", [])
                for item in search_items:
                    clean_snippet = re.sub(r"<[^>]+>", "", item.get("snippet", ""))
                    results.append(f"• {item.get('title')}: {clean_snippet}")
        except Exception as e:
            logger.warning(f"Wikipedia search warning: {e}")

        # 2. Consulta de respuestas rápidas DuckDuckGo
        try:
            ddg_encoded = urllib.parse.quote(query)
            ddg_url = f"https://api.duckduckgo.com/?q={ddg_encoded}&format=json&no_html=1&skip_disambig=1"
            req = urllib.request.Request(
                ddg_url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                abstract = data.get("AbstractText", "")
                if abstract:
                    results.append(f"• DuckDuckGo Instant Answer: {abstract}")
                
                # Related topics
                topics = data.get("RelatedTopics", [])
                for t in topics[:2]:
                    if isinstance(t, dict) and "Text" in t:
                        results.append(f"• {t.get('Text')}")
        except Exception as e:
            logger.warning(f"DuckDuckGo search warning: {e}")

        # 3. Fallback inteligente si no hay resultados específicos
        if not results:
            return "No se encontraron resultados web directos para esta consulta."

        combined = "\n".join(results[:max_results + 1])
        logger.info(f"✅ [WebSearch] {len(results)} evidencias recuperadas.")
        return combined

    @property
    def provider_name(self) -> str:
        return "DuckDuckGo / Wikipedia (Zero-Cost Web Search)"
