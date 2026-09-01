# 🏛️ Architecture Decision Record: ADR-0013 - Despachador Parametrizado de Herramientas y Barrera Anti-Rechazo

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-014`](../use-cases/UC-014-zero-refusal-autonomous-tool-dispatch.md)

---

## 1. Contexto y Problema
Las solicitudes conversacionales de los usuarios contienen parámetros implícitos o explícitos (horas, títulos, referencias temporales). Si el motor de intenciones es rígido, no dispara la herramienta y el LLM produce rechazos estándar (*"Lo siento, no puedo cumplir..."*).

---

## 2. Decisión
1. Incorporar analizadores semánticos mediante expresiones regulares y raíces morfológicas para extraer horas (`\d{1,2}:\d{2}`), títulos y acciones de prueba/revisión.
2. Extender `MCPRuntimePort` con `create_calendar_event(title, time, date)`.
3. Implementar un guardián de salida (*Zero-Refusal Guard*) que detecte patrones de rechazo del LLM y los reemplace por la confirmación ejecutada de la herramienta.

---

## 3. Consecuencias
- Cero rechazos o excusas por parte del asistente.
- Ejecución fiel con los parámetros solicitados por el usuario.
