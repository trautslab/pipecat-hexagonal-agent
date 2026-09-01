# 🎯 Caso de Uso: UC-020 - Enrutador Cognitivo Unificado 100% LLM-First

- **ID:** `UC-020`
- **Dominio:** LLM-First Architecture / Cognitive Function Calling / Zero-Heuristic ReAct
- **Actor Principal:** Usuario / LLM (Llama 3.1) / Runtime MCP / GoogleCalendarClient
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-018`](../diagrams/sequences/SEQ-018-unified-llm-router-and-tool-orchestrator.md)
- **Contrato de Tarea:** [`TASK-022`](../../.agents/tasks/TASK-022-unified-llm-router.md)

---

## 📖 Descripción
Se traslada el 100% del enrutamiento de intenciones, selección de herramientas y generación de metadatos al modelo de lenguaje LLM (`llama3.1:8b`), eliminando completamente listas fijas de palabras, saludos o patrones regex en Python.
