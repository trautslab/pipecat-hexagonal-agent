# 🎯 Caso de Uso: UC-017 - Razonamiento Nativo del LLM y Reglas de Proactividad

- **ID:** `UC-017`
- **Dominio:** LLM Function Calling / ReAct Autonomous Reasoning / Best Practices
- **Actor Principal:** Usuario / LLM (Llama 3.1) / Runtime MCP
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-015`](../diagrams/sequences/SEQ-015-llm-native-tool-dispatch.md)
- **Contrato de Tarea:** [`TASK-019`](../../.agents/tasks/TASK-019-llm-native-tool-calling.md)

---

## 📖 Descripción
El modelo LLM asume la responsabilidad de razonar sobre la solicitud del usuario, extrayendo parámetros estructurados (título, fecha, hora, ubicación) y aplicando proactivamente reglas de mejores prácticas para generar descripciones amables y detalladas con emojis antes de invocar la herramienta correspondiente.
