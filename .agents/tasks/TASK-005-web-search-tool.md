# 📋 Contrato de Tarea: TASK-005 - Herramienta de Búsqueda Web y Grounding Factual

- **ID de Tarea:** `TASK-005`
- **Caso de Uso Relacionado:** [`UC-005`](../../docs/use-cases/UC-005-web-search-grounded-qa.md)
- **Especificación Técnica:** [`SPEC-001`](../../docs/specs/SPEC-001-voice-agent-contract.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar `SearchPort`, `DuckDuckGoSearchAdapter` y `GroundingService` para dotar al agente de voz de acceso a internet en tiempo real, garantizando respuestas factuales libres de alucinaciones.

---

## 📐 Criterios de Aceptación (BDD / Gherkin)

```gherkin
Scenario: Respuesta a pregunta de ubicación con búsqueda web
  Given el servicio GroundingService conectado a DuckDuckGoSearchAdapter
  When el usuario pregunta "¿Dónde queda la Universidad Nacional de Ingeniería del Perú?"
  Then el SearchPort ejecuta la búsqueda y recupera la dirección exacta (Rímac / Av. Túpac Amaru)
  And el LLM genera una respuesta precisa basada en los hechos recuperados
```

---

## 🧪 Comando de Evaluación (Eval Command)
```bash
python3 evals/harness.py --task TASK-005
```
