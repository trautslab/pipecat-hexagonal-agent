# 🏛️ Architecture Decision Record: ADR-0016 - Razonamiento de Parámetros Nativo del LLM y Reglas de Proactividad

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-017`](../use-cases/UC-017-llm-native-tool-calling-and-proactive-reasoning.md)

---

## 1. Contexto y Problema
El sistema delegaba parte del parseo de lenguaje natural a heurísticas de código rígidas. Para lograr un comportamiento de agente autónomo genuino y proactivo, el modelo de lenguaje (LLM) debe ser el responsable directo de razonar sobre la solicitud, estructurar los argumentos y redactar el contenido enriquecido.

---

## 2. Decisión
1. Implementar un paso de razonamiento nativo (`llm_reason_and_extract_tool_call`) dentro del ciclo ReAct de `AutonomousReasoningEngine`.
2. Establecer un System Prompt de Razonamiento Estructurado con reglas de excelencia y mejores prácticas (redacción proactiva de descripciones con emojis, inferencia de ubicaciones y normalización de fecha/hora).
3. Mantener un fallback determinista para resiliencia ante caídas de red o tiempo de espera.

---

## 3. Consecuencias
- Extracción de parámetros flexible e inteligente respaldada por el modelo de IA.
- Proactividad inherente en la redacción de notas y recordatorios.
- Trazabilidad transparente en la consola ReAct en tiempo real.
