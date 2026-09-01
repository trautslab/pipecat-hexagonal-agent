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
  - [`ADR-0008`: Consola Lateral Derecha de Trazabilidad en Tiempo Real](adr/ADR-0008-right-sidebar-live-console-architecture.md)
  - [`ADR-0009`: Ejecución Activa y Verificación de Herramientas MCP](adr/ADR-0009-mcp-tool-execution-client.md)
  - [`ADR-0010`: Runtime Autónomo de MCPs y Prohibición de Comandos Manuales](adr/ADR-0010-autonomous-mcp-subprocess-runtime.md)
  - [`ADR-0011`: Persistencia de Estado y Telemetría en el Backend](adr/ADR-0011-client-agnostic-server-side-persistence.md)
  - [`ADR-0012`: Rediseño de Interfaz a Layout Postman / Modern IDE Workbench](adr/ADR-0012-postman-ide-workbench-ui.md)
  - [`ADR-0013`: Despachador Parametrizado de Herramientas y Barrera Anti-Rechazo](adr/ADR-0013-parameterized-tool-dispatch-and-anti-refusal-guard.md)

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
| [`UC-009`](use-cases/UC-009-realtime-telemetry-console-sidebar.md) | Consola Lateral Derecha en Tiempo Real | Observability | [`SEQ-007`](diagrams/sequences/SEQ-007-realtime-trace-streaming.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-011`](../.agents/tasks/TASK-011-realtime-console-right-sidebar.md) | `APPROVED` |
| [`UC-010`](use-cases/UC-010-mcp-active-tool-execution.md) | Ejecución Activa de Herramientas MCP | Automation | [`SEQ-008`](diagrams/sequences/SEQ-008-mcp-live-tool-invocation.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-012`](../.agents/tasks/TASK-012-mcp-active-executor.md) | `APPROVED` |
| [`UC-011`](use-cases/UC-011-autonomous-mcp-execution-engine.md) | Motor Autónomo y Cero Comandos Manuales | Autonomous Agent | [`SEQ-009`](diagrams/sequences/SEQ-009-autonomous-tool-runner.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-013`](../.agents/tasks/TASK-013-autonomous-mcp-runtime.md) | `APPROVED` |
| [`UC-012`](use-cases/UC-012-server-side-session-telemetry-persistence.md) | Persistencia de Estado en Servidor | Persistence | [`SEQ-010`](diagrams/sequences/SEQ-010-backend-session-sync.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-014`](../.agents/tasks/TASK-014-server-side-persistence.md) | `APPROVED` |
| [`UC-013`](use-cases/UC-013-ide-workbench-layout.md) | Layout IDE Workbench (Postman Style) | UI/UX Layout | [`SEQ-011`](diagrams/sequences/SEQ-011-ide-workbench-interaction.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-015`](../.agents/tasks/TASK-015-ide-workbench-layout.md) | `APPROVED` |
| [`UC-014`](use-cases/UC-014-zero-refusal-autonomous-tool-dispatch.md) | Despacho Parametrizado & Anti-Rechazo | Tool Dispatch | [`SEQ-012`](diagrams/sequences/SEQ-012-parameterized-mcp-tool-dispatch.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-016`](../.agents/tasks/TASK-016-parameterized-autonomous-tool-dispatch.md) | `APPROVED` |

---

## 📊 3. Catálogo de Diagramas por Tipo

### Diagramas de Secuencia (`docs/diagrams/sequences/`)
- [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) — Flujo streaming de tramas de audio entre transporte, STT, LLM, TTS y altavoces.
- [`SEQ-002`](diagrams/sequences/SEQ-002-websocket-client-streaming.md) — Streaming de audio y subtítulos bidireccional por WebSocket con cliente web.
- [`SEQ-003`](diagrams/sequences/SEQ-003-tool-calling-search.md) — Flujo de invocación de búsqueda web e inyección de evidencias en el LLM.
- [`SEQ-004`](diagrams/sequences/SEQ-004-session-resumption-and-tool-generation.md) — Reanudación de sesiones y scaffolding de adaptadores.
- [`SEQ-005`](diagrams/sequences/SEQ-005-react-reasoning-and-mcp-installation.md) — Ciclo de razonamiento ReAct multi-paso y autoinstalación dinámica de servidores MCP.
- [`SEQ-006`](diagrams/sequences/SEQ-006-action-trace-inspector.md) — Streaming de eventos de telemetría y exportación al portapapeles.
- [`SEQ-007`](diagrams/sequences/SEQ-007-realtime-trace-streaming.md) — Streaming en tiempo real a la consola lateral derecha de trazabilidad.
- [`SEQ-008`](diagrams/sequences/SEQ-008-mcp-live-tool-invocation.md) — Invocación y ejecución activa de herramientas MCP (Google Calendar).
- [`SEQ-009`](diagrams/sequences/SEQ-009-autonomous-tool-runner.md) — Ejecución autónoma de subprocesos MCP y eliminación de directivas pasivas.
- [`SEQ-010`](diagrams/sequences/SEQ-010-backend-session-sync.md) — Sincronización y persistencia de sesiones y telemetría en backend.
- [`SEQ-011`](diagrams/sequences/SEQ-011-ide-workbench-interaction.md) — Flujo de interacción en layout Postman/IDE Workbench.
- [`SEQ-012`](diagrams/sequences/SEQ-012-parameterized-mcp-tool-dispatch.md) — Despacho de herramientas parametrizadas y barrera anti-rechazo.

### Diagramas de Actividad / Flujos (`docs/diagrams/activities/`)
- [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) — Lógica de detección de voz del usuario durante la reproducción del bot e interrupción inmediata (*Barge-in*).

### Máquinas de Estados (`docs/diagrams/state-machines/`)
- [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) — Ciclo de vida y transiciones del agente (`IDLE` -> `LISTENING` -> `THINKING` -> `SPEAKING` -> `INTERRUPTED`).

---

## 📝 4. Especificaciones Técnicas (RFCs / Specs)
- [`SPEC-001`](specs/SPEC-001-voice-agent-contract.md) — Especificación técnica del contrato de puertos, adaptadores y pipeline de Pipecat.
