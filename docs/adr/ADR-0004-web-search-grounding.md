# 🏛️ Architecture Decision Record: ADR-0004 - Integración de SearchPort y Grounding en Tiempo Real

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-005`](../use-cases/UC-005-web-search-grounded-qa.md)

---

## 1. Contexto y Problema
Los modelos de lenguaje locales (incluso modelos de 8B o 14B) pueden presentar alucinaciones o desconocer datos específicos sobre direcciones, noticias de última hora o detalles geográficos hiperlocales (como distritos y avenidas de universidades en Perú). 

Confiar ciegamente en los pesos paramétricos del LLM degrada la confiabilidad del asistente de voz.

---

## 2. Decisión
1. Diseñar el puerto abstracto `SearchPort` en `core/ports/search_port.py`.
2. Implementar `DuckDuckGoSearchAdapter` en `adapters/tools/duckduckgo_search_adapter.py` para realizar búsquedas web en vivo a costo $0 sin requerir API keys comerciales ni registro previo.
3. Crear `GroundingService` en `core/services/grounding_service.py` para orquestar la búsqueda y alimentar al LLM con fragmentos de internet verificados en tiempo real.

---

## 3. Consecuencias

### Positivas:
- Cero alucinaciones en preguntas factuales, institucionales o geográficas.
- Acceso a información actualizada en tiempo real sin reentrenar ni fine-tunear modelos.
- Cumple con la Arquitectura Hexagonal y la política de costo cero ($0).

### Negativas / Trade-offs:
- Añade una pequeña latencia de red (~200ms - 400ms) durante la consulta HTTP de búsqueda.
