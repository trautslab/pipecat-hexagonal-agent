# 🏛️ Architecture Decision Record: ADR-0019 - Enrutamiento Cognitivo 100% LLM-First y Eliminación de Heurísticas

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-020`](../use-cases/UC-020-unified-llm-first-cognitive-router.md)

---

## 1. Contexto y Problema
El uso de listas fijas de palabras (saludos, verbos de acción, diccionarios de meses o listas de triggers) genera fragilidad ante la variabilidad infinita del lenguaje natural humano y viola el principio de autonomía cognitiva de un agente moderno.

---

## 2. Decisión
1. **Eliminación Total de Heurísticas y Listas Estáticas:** Suprimir cualquier lista fija de palabras (`hola`, `buenos días`, `crear`, etc.) y regexes manuales en el código Python de backend.
2. **Adopción de Enrutador Cognitivo Unificado:** Cada interacción del usuario es evaluada por el LLM (`llama3.1:8b`) mediante un meta-prompt de razonamiento estructurado ReAct que clasifica la herramienta adecuada (`google_calendar.create_event`, `google_calendar.list_events`, `google_calendar.delete_event`, `mcp_manager.install_mcp`, `web_search`, `none`).
3. **Proactividad de Formato en el LLM:** El LLM genera de forma autónoma el título exacto, fecha normalizada (YYYY-MM-DD), hora en 24h (HH:MM:SS), ubicación y una descripción amable con emojis.

---

## 3. Consecuencias
- Cero fallos por sinónimos o frases coloquiales no previstas.
- Flexibilidad total ante cualquier idioma o estilo de habla del usuario.
- Arquitectura pura y mantenible alineada a estándares OpenClaw y OpenAI Function Calling.
