# 🏛️ Architecture Decision Record: ADR-0007 - Desplegable de Telemetría e Inspección de Acciones en la UI

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-008`](../use-cases/UC-008-action-inspector-telemetry.md)

---

## 1. Contexto y Problema
Para depurar y perfeccionar el comportamiento de un agente autónomo estilo OpenClaw, el usuario necesita visibilidad transparente de todas las decisiones intermedias tomadas por el sistema (consultas web realizadas, archivos modificados, parámetros de herramientas invocadas y latencias) sin saturar visualmente el flujo principal de conversación.

---

## 2. Decisión
1. Enriquecer los eventos emitidos por el servidor con trazas de telemetría detalladas (timestamps, latencias, payloads de herramientas y archivos tocados).
2. Renderizar un elemento colapsable `<details class="action-inspector">` en cada burbuja del asistente.
3. Integrar un botón dedicado `[📋 Copiar Registro]` que serialice la traza técnica en formato Markdown legible para facilitar el feedback.

---

## 3. Consecuencias
- 100% de transparencia y observabilidad sobre las acciones del agente.
- Facilidad máxima para recopilar y reportar trazas de depuración con un solo clic.
