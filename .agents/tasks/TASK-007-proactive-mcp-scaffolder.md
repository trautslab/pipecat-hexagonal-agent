# 📋 Contrato de Tarea: TASK-007 - Autoconocimiento del Sistema y Scaffolding Proactivo de MCPs

- **ID de Tarea:** `TASK-007`
- **Caso de Uso:** [`UC-006`](../../docs/use-cases/UC-006-chat-persistence-and-mcp-scaffolding.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Dota al asistente **Aura** de autoconocimiento de su propia arquitectura (`pipecat-hexagonal-agent`), eliminando respuestas derrotistas ("no puedo hacer eso") y permitiéndole formular planes concretos, configuraciones en `.env` y código de adaptadores para herramientas y servidores MCP (ej. Google Calendar).

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Solicitud de integración de Google Calendar MCP
  When el usuario pregunta a Aura sobre cómo integrarse con Google Calendar
  Then Aura responde proactivamente explicando la integración con el protocolo MCP
  And indica qué variables configurar en .env (ej. GOOGLE_CALENDAR_CREDENTIALS_JSON)
  And explica cómo registrar el servidor en .agents/mcp/mcp-servers.json
```
