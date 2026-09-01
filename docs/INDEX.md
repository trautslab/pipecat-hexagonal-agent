# 🗺️ Índice Maestro de Documentación & Trazabilidad (AI-SDLC)

Este índice actúa como la **matriz de navegación maestra** para todo el catálogo de arquitectura, casos de uso, especificaciones y diagramas del proyecto `pipecat-hexagonal-agent`.

---

## 🏛️ 1. Arquitectura Global
- [Modelo C4 (Contexto, Contenedores, Componentes)](architecture/c4-model.md)
- [Arquitectura Hexagonal & Patrón Ports/Adapters](architecture/hexagonal-architecture.md)
- [Decisiones de Arquitectura (ADRs)](adr/ADR-0001-hexagonal-architecture-pipecat.md)
  - [`ADR-0001`: Adopción de Arquitectura Hexagonal sobre Pipecat](adr/ADR-0001-hexagonal-architecture-pipecat.md)
  - [`ADR-0002`: Selección de Pila Local Gratuita (Whisper + Ollama + Piper)](adr/ADR-0002-zero-cost-local-stack.md)

---

## 🎯 2. Matriz de Trazabilidad: Casos de Uso vs Diagramas

| ID Caso de Uso | Título | Dominio | Diagrama Secuencia | Diagrama Actividad | Máquina Estados | Contrato Tarea | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [`UC-001`](use-cases/UC-001-realtime-voice-conversation.md) | Conversación de Voz en Tiempo Real | Core/Audio | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-001`](../.agents/tasks/TASK-001-hexagonal-core.md) | `APPROVED` |
| [`UC-002`](use-cases/UC-002-zero-cost-local-execution.md) | Ejecución Local Offline Gratuita | Local AI | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-002`](../.agents/tasks/TASK-002-zero-cost-local-adapters.md) | `APPROVED` |
| [`UC-003`](use-cases/UC-003-cloud-hybrid-switch.md) | Conmutación Cloud e Híbrida | Cloud AI | [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) | [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) | [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) | [`TASK-003`](../.agents/tasks/TASK-003-cloud-hybrid-adapters.md) | `APPROVED` |

---

## 📊 3. Catálogo de Diagramas por Tipo

### Diagramas de Secuencia (`docs/diagrams/sequences/`)
- [`SEQ-001`](diagrams/sequences/SEQ-001-voice-streaming-pipeline.md) — Flujo streaming de tramas de audio entre transporte, STT, LLM, TTS y altavoces.

### Diagramas de Actividad / Flujos (`docs/diagrams/activities/`)
- [`ACT-001`](diagrams/activities/ACT-001-audio-barge-in-interruption.md) — Lógica de detección de voz del usuario durante la reproducción del bot e interrupción inmediata (*Barge-in*).

### Máquinas de Estados (`docs/diagrams/state-machines/`)
- [`STM-001`](diagrams/state-machines/STM-001-agent-session-lifecycle.md) — Ciclo de vida y transiciones del agente (`IDLE` -> `LISTENING` -> `THINKING` -> `SPEAKING` -> `INTERRUPTED`).

---

## 📝 4. Especificaciones Técnicas (RFCs / Specs)
- [`SPEC-001`](specs/SPEC-001-voice-agent-contract.md) — Especificación técnica del contrato de puertos, adaptadores y pipeline de Pipecat.
