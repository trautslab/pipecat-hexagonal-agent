# 🎯 Caso de Uso: UC-011 - Motor Autónomo de Ejecución de MCPs y Cero Directivas Manuales

- **ID:** `UC-011`
- **Dominio:** Autonomous Tool Calling / Subprocess Execution
- **Actor Principal:** Usuario / Agente de Software (Aura)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-009`](../diagrams/sequences/SEQ-009-autonomous-tool-runner.md)
- **Contrato de Tarea:** [`TASK-013`](../../.agents/tasks/TASK-013-autonomous-mcp-runtime.md)

---

## 📖 Descripción
El agente de voz opera de forma 100% autónoma. Cuando se requiere verificar, sincronizar, consultar o ejecutar acciones sobre herramientas MCP (como Google Calendar):
1. El agente **ejecuta internamente el subproceso o llamada a herramienta** utilizando `MCPRuntimeAdapter`.
2. Tiene **estrictamente prohibido delegar comandos de terminal al usuario** (ej. `npm run sync-google-calendar`, `npm run setup`, `revisa logs/...`).
3. Retorna directamente al usuario los resultados de la ejecución real (eventos agendados, confirmación de sincronización, IDs de respuesta y métricas).
