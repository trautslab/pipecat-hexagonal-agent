# 🗺️ Índice Maestro de Documentación & Trazabilidad (AI-SDLC)

Este índice actúa como la **matriz de navegación maestra** para todo el catálogo de arquitectura, casos de uso, especificaciones y diagramas del proyecto `pipecat-hexagonal-agent`.

---

## 🏛️ 1. Arquitectura Global
- [Modelo C4 (Contexto, Contenedores, Componentes)](architecture/c4-model.md)
- [Arquitectura Hexagonal & Patrón Ports/Adapters](architecture/hexagonal-architecture.md)
- [Decisiones de Arquitectura (ADRs)](adr/ADR-0001-hexagonal-architecture-pipecat.md)
  - [`ADR-0001`: Adopción de Arquitectura Hexagonal sobre Pipecat](adr/ADR-0001-hexagonal-architecture-pipecat.md)
  - [`ADR-0002`: Selección de Pila Local Gratuita (Whisper + Ollama + Piper)](adr/ADR-0002-zero-cost-local-stack.md)
  - [`ADR-0003`: Arquitectura de Transporte WebSocket para Cliente Web](adr/ADR-0003-websocket-web-client-architecture.md)
  - [`ADR-0004`: Integración de SearchPort y Grounding en Tiempo Real](adr/ADR-0004-web-search-grounding.md)
  - [`ADR-0005`: Persistencia de Conversaciones y Autoconocimiento de MCPs](adr/ADR-0005-chat-history-persistence-and-mcp-integration.md)
  - [`ADR-0006`: Motor ReAct y Gestor Autónomo de MCPs estilo OpenClaw](adr/ADR-0006-openclaw-reasoning-and-dynamic-mcp.md)
  - [`ADR-0007`: Desplegable de Telemetría e Inspección de Acciones en la UI](adr/ADR-0007-action-inspector-ui.md)

---

## 🎯 2. Matriz de Trazabilidad: Casos de Uso vs Diagramas

| ID Caso de Uso | Título | Dominio | Diagrama Secuencia | Diagrama Actividad | Máquina Estados | Contrato Tarea | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`UC-001`](use-cases/UC-001-realtime-voice-conversation.md) | Conversación de Voz en Tiempo Real | Core/Audio | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-001`](../.agents/tasks/TASK-001-hexagonal-core.md) | `APPROVED` |
| [`UC-002`](use-cases/UC-002-zero-cost-local-execution.md) | Ejecución Local Offline Gratuita | Local AI | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-002`](../.agents/tasks/TASK-002-zero-cost-local-adapters.md) | `APPROVED` |
| [`UC-003`](use-cases/UC-003-cloud-hybrid-switch.md) | Conmutación Cloud e Híbrida | Cloud AI | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-003`](../.agents/tasks/TASK-003-cloud-hybrid-adapters.md) | `APPROVED` |
| [`UC-004`](use-cases/UC-004-web-browser-voice-interaction.md) | Interacción de Voz en Navegador Web | Web/WS | [`SEQ-002`](diagrams/sequences/SEQ-002-websocket-client-streaming.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-004`](../.agents/tasks/TASK-004-web-interface-websocket.md) | `APPROVED` |
| [`UC-005`](use-cases/UC-005-web-search-grounded-qa.md) | Grounding Factual con Búsqueda Web | Tools/Grounding | [`SEQ-003`](diagrams/sequences/SEQ-003-tool-calling-search.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-005`](../.agents/tasks/TASK-005-web-search-tool.md) | `APPROVED` |
| [`UC-006`](use-cases/UC-006-chat-persistence-and-mcp-scaffolding.md) | Persistencia de Chats y UI Copiado | UI/Chat | [`SEQ-004`](diagrams/sequences/SEQ-004-session-resumption-and-tool-generation.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-006`](../.agents/tasks/TASK-006-chat-history-and-copy-actions.md), [`TASK-007`](../.agents/tasks/TASK-007-proactive-mcp-scaffolder.md) | `APPROVED` |
| [`UC-007`](use-cases/UC-007-openclaw-autonomous-reasoning-mcp.md) | Motor ReAct y Autoinstalación MCP | OpenClaw/Agent | [`SEQ-005`](diagrams/sequences/SEQ-005-react-reasoning-and-mcp-installation.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-008`](../.agents/tasks/TASK-008-autonomous-react-engine.md), [`TASK-009`](../.agents/tasks/TASK-009-dynamic-mcp-manager.md) | `APPROVED` |
| [`UC-008`](use-cases/UC-008-action-inspector-telemetry.md) | Inspector de Acciones y Telemetría UI | Observability | [`SEQ-006`](diagrams/sequences/SEQ-006-action-trace-inspector.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-010`](../.agents/tasks/TASK-010-action-inspector-dropdown.md) | `APPROVED` |

---

## 📊 3. Catálogo de Diagramas por Tipo

### Diagramas de Secuencia (`docs/diagrams/sequences/`)
- [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) — Flujo streaming de tramas de audio entre transporte, STT, LLM, TTS y altavoces.
- [`SEQ-002`](diagrams/sequences/SEQ-002-websocket-client-streaming.md) — Streaming de audio y subtítulos bidireccional por WebSocket con cliente web.
- [`SEQ-003`](diagrams/sequences/SEQ-003-tool-calling-search.md) — Flujo de invocación de búsqueda web e inyección de evidencias en el LLM.
- [`SEQ-004`](diagrams/sequences/SEQ-004-session-resumption-and-tool-generation.md) — Reanudación de sesiones y scaffolding de adaptadores.
- [`SEQ-005`](diagrams/sequences/SEQ-005-react-reasoning-and-mcp-installation.md) — Ciclo de razonamiento ReAct multi-paso y autoinstalación dinámica de servidores MCP.
- [`SEQ-006`](diagrams/sequences/SEQ-006-action-trace-inspector.md) — Streaming de eventos de telemetría y exportación al portapapeles.

### Diagramas de Actividad / Flujos (`docs/diagrams/activities/`)
- [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) — Lógica de detección de voz del usuario durante la reproducción del bot e interrupción inmediata (*Barge-in*).

### Máquinas de Estados (`docs/diagrams/state-machines/`)
- [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) — Ciclo de vida y transiciones del agente (`IDLE` -> `LISTENING` -> `THINKING` -> `SPEAKING` -> `INTERRUPTED`).

---

## 📝 4. Especificaciones Técnicas (RFCs / Specs)
- [`SPEC-001`](specs/SPEC-001-voice-agent-contract.md) — Especificación técnica del contrato de puertos, adaptadores y pipeline de Pipecat.
