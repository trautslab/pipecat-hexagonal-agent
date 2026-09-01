# 🎯 Caso de Uso: UC-007 - Motor de Razonamiento ReAct y Autoinstalación de MCPs (Estilo OpenClaw)

- **ID:** `UC-007`
- **Dominio:** Autonomous Agent / ReAct Reasoning / Dynamic MCP Tools
- **Actor Principal:** Usuario (Interlocutor / Desarrollador)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-005`](../diagrams/sequences/SEQ-005-react-reasoning-and-mcp-installation.md)
- **Contratos de Tarea:** [`TASK-008`](../../.agents/tasks/TASK-008-autonomous-react-engine.md) y [`TASK-009`](../../.agents/tasks/TASK-009-dynamic-mcp-manager.md)

---

## 📖 Descripción
El usuario solicita una capacidad externa que el asistente no posee de forma nativa (ej. *"Quisiera usar Google Calendar o que te instales el MCP correspondiente en tu sistema"*). 
En lugar de responder con una negativa o limitarse a dar un tutorial, el agente activa su **Motor de Razonamiento Autónomo ReAct**:
1. Formula un pensamiento (*Thought*).
2. Ejecuta una búsqueda web (*Action: WebSearch*) para identificar el paquete MCP oficial o servidor adecuado.
3. Invoca la herramienta de autoinstalación (*Action: MCPManager*) que registra el servidor en `.agents/mcp/mcp-servers.json` y declara las variables requeridas en `.env`.
4. Evalúa la observación (*Observation*) y le responde al usuario con la confirmación de la instalación, especificando únicamente qué credenciales debe completar en `.env`.
