# 🎯 Caso de Uso: UC-006 - Persistencia de Conversaciones y Scaffolding Proactivo de MCPs

- **ID:** `UC-006`
- **Dominio:** UI / Session Persistence / MCP Tool Scaffolding
- **Actor Principal:** Usuario (Interlocutor / Desarrollador)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-004`](../diagrams/sequences/SEQ-004-session-resumption-and-tool-generation.md)
- **Contratos de Tarea:** [`TASK-006`](../../.agents/tasks/TASK-006-chat-history-and-copy-actions.md) y [`TASK-007`](../../.agents/tasks/TASK-007-proactive-mcp-scaffolder.md)

---

## 📖 Descripción
1. El usuario puede interactuar con múltiples sesiones conversacionales a través de una interfaz estilo ChatGPT / Claude UI con panel lateral de historial.
2. Cada mensaje puede copiarse al portapapeles con un solo clic.
3. El agente de voz tiene autoconocimiento de su propia arquitectura de software (`pipecat-hexagonal-agent`), sabe cómo integrar servidores MCP (Model Context Protocol) como Google Calendar, y actúa como un ingeniero de software proactivo guiando la configuración de adaptadores y dejando al usuario únicamente la definición de credenciales en `.env`.
4. El historial de mensajes se preserva para retomar cualquier conversación previa con memoria multi-turno completa.
