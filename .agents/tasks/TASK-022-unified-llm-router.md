# 📋 Contrato de Tarea: TASK-022 - Enrutador Cognitivo Unificado 100% LLM-First

- **ID de Tarea:** `TASK-022`
- **Caso de Uso:** [`UC-020`](../../docs/use-cases/UC-020-unified-llm-first-cognitive-router.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Refactorizar `AutonomousReasoningEngine` y `GroundingService` eliminando cualquier lista estática de palabras o regexes manuales en Python, delegando el 100% de la clasificación de intenciones y generación estructurada al LLM (`llama3.1:8b`).

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Solicitud conversacional procesada puramente por el LLM
  Given una solicitud con lenguaje coloquial o complejo
  When AutonomousReasoningEngine invoca al LLM como enrutador cognitivo
  Then el LLM emite un JSON con thought, tool y parameters
  And no se utilizan listas de palabras estáticas en Python
  And la herramienta seleccionada se despacha con los parámetros generados por el LLM
```
