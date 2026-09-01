# 🏛️ Architecture Decision Record: ADR-0006 - Motor ReAct y Gestor Autónomo de MCPs estilo OpenClaw

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-007`](../use-cases/UC-007-openclaw-autonomous-reasoning-mcp.md)

---

## 1. Contexto y Problema
Los asistentes tradicionales son pasivos y responden con disculpas cuando no tienen una herramienta instalada. Los sistemas avanzados como OpenClaw, OpenHands y Devin ejecutan bucles de pensamiento-acción (ReAct) para buscar el protocolo MCP de la herramienta solicitada e instalarla automáticamente.

---

## 2. Decisión
1. Implementar `AutonomousReasoningEngine` en `core/services/reasoning_engine.py` para manejar el ciclo multi-paso: Pensamiento -> Búsqueda Web -> Instalación MCP -> Reflexión -> Respuesta.
2. Crear `MCPManagerAdapter` en `adapters/tools/mcp_manager_adapter.py` para descubrir paquetes en npm/GitHub, escribir en `.agents/mcp/mcp-servers.json` y declarar variables en `.env`.
3. Emitir eventos de pensamiento al cliente web para renderizar las etapas del razonamiento en tiempo real.

---

## 3. Consecuencias
- El asistente pasa de ser un bot pasivo a un agente autónomo de ingeniería capaz de auto-extenderse.
- Se mantiene el cumplimiento con la Arquitectura Hexagonal y la gobernanza AI-SDLC.
