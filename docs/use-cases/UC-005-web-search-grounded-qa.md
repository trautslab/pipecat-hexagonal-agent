# 🎯 Caso de Uso: UC-005 - Preguntas Factuales con Búsqueda Web en Tiempo Real (Grounding)

- **ID:** `UC-005`
- **Dominio:** Tools / Web Grounding / Anti-Hallucination
- **Actor Principal:** Usuario (Interlocutor)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-003`](../diagrams/sequences/SEQ-003-tool-calling-search.md)
- **Contrato de Tarea:** [`TASK-005`](../../.agents/tasks/TASK-005-web-search-tool.md)

---

## 📖 Descripción
Cuando el usuario formula una pregunta sobre datos fácticos, ubicaciones geográficas, direcciones de instituciones o información actualizada (ej. *"¿Dónde queda la Universidad Nacional de Ingeniería del Perú?"*), el agente no se fía de su conocimiento estático interno. En su lugar, activa el servicio de búsqueda web en tiempo real (`SearchPort`), recupera las fuentes y fragmentos verificados de internet, y le proporciona esa evidencia al LLM para generar una respuesta exacta y sin alucinaciones.

---

## 📋 Precondiciones
1. El `SearchPort` y el adaptador `DuckDuckGoSearchAdapter` están configurados y disponibles.
2. El servicio `GroundingService` intercepta o asiste al generador de respuestas.

---

## 🔄 Flujo Principal (Happy Path)
1. El usuario pregunta por voz: *"¿Dónde queda la Universidad Nacional de Ingeniería?"*.
2. El `GroundingService` detecta la necesidad de verificación factual.
3. Se invoca `SearchPort.search("Universidad Nacional de Ingeniería Perú ubicación dirección")`.
4. El motor de búsqueda devuelve fragmentos verificados: *"Ubicación: Av. Túpac Amaru 210, Rímac, Lima, Perú"*.
5. Se inyecta la evidencia en el contexto del LLM.
6. El LLM responde: *"La Universidad Nacional de Ingeniería (UNI) se encuentra en la Av. Túpac Amaru 210, en el distrito del Rímac, Lima, Perú."*
7. La respuesta se transmite por streaming de voz al usuario.
