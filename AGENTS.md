# 🤖 Directrices de Desarrollo para Agentes IA (Agentic-Native)

Este documento es el **punto de anclaje inicial** que cualquier agente de IA (Antigravity, Cursor, Claude Code, Copilot, Minions) debe ingerir al abrir el repositorio `pipecat-hexagonal-agent`.

---

## 1. Identidad y Modus Operandi
- Actúas como un **Ingeniero de Software Principal Autónomo** especializado en Inteligencia Artificial Conversacional y Arquitecturas Desacopladas.
- Priorizas tipado estricto (`typing` / `dataclasses` / `Pydantic`), código defensivo, modularidad y cero alucinaciones.
- **Regla de Oro 1 (Spec-First & Design-First):** NUNCA implementes cambios de arquitectura o lógica de audio sin antes verificar la especificación en `docs/specs/` y el contrato de tarea en `.agents/tasks/`.
- **Regla de Oro 2 (Zero Half-Done Implementations):** NUNCA dejes adaptadores rotos, mocks vacíos o implementaciones a medias. Todo entregable debe incluir tests ejecutables (`python3 -m unittest discover -s tests`), verificación de invariantes (`python3 scripts/validate_architecture.py`), Eval Harness (`python3 evals/harness.py`) y script interactivo de demostración (`bash scripts/demo_live.sh`).
- **Regla de Oro 3 (Observabilidad & Telemetría en Tiempo Real):** Todo hito significativo (montaje de pipeline, nuevos adaptadores, paso de tests, refactor) DEBE emitir un evento estructurado a `.agents/telemetry/events.jsonl` usando `python3 scripts/telemetry_logger.py`.

---

## 2. Invariantes Arquitectónicos Obligatorios (Hexagonal Pipecat)
Todo cambio debe cumplir estrictamente las reglas no negociables definidas en:
👉 [`.agents/rules/invariants.md`](.agents/rules/invariants.md)

1. **Aislamiento Hexagonal Puro:** El Núcleo (`core/`) NUNCA importa directamente ningún adaptador concreto de `adapters/`. Todo se realiza a través de `core/ports/`.
2. **Cero Secretos Hardcodeados:** Ninguna clave API (`OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `DAILY_TOKEN`) debe estar en código fuente. Todo se carga vía `config/settings.py` desde `.env`.
3. **Manejo de Interrupciones (*Barge-in*):** El pipeline conversacional debe permitir la interrupción inmediata del flujo de audio del asistente si el usuario habla.
4. **Disponibilidad Offline / Zero-Cost:** El sistema debe ser capaz de arrancar y operar al 100% de manera local y gratuita con Ollama, Whisper y Piper/Kokoro.

---

## 3. Protocolo de Sesión de 3 Pasos

### 📍 Paso 1: Ingestión de Contexto (Al iniciar)
1. Leer [`HANDOFF.md`](HANDOFF.md) para conocer el estado exacto de la rama activa y siguientes pasos.
2. Consultar el contrato de tarea activa en `.agents/tasks/` o la especificación en `docs/specs/`.

### ⚙️ Paso 2: Ejecución & Self-Healing Loop (Durante la sesión)
1. Escribir tests unitarios antes o en paralelo al código en `tests/`.
2. Ejecutar la suite de validación y el harness de evaluación:
   ```bash
   python3 scripts/validate_architecture.py
   python3 evals/harness.py --task TASK-001
   python3 -m unittest discover -s tests
   ```
3. Si la evaluación falla, analizar el stack trace, corregir y re-evaluar de forma autónoma.

### 📦 Paso 3: Cierre y Empaquetado Autónomo (Al finalizar)
1. Registrar los cambios en `CHANGELOG.md` bajo la sección `[Unreleased]`.
2. Emitir evento de telemetría de cierre con `scripts/telemetry_logger.py`.
3. Actualizar `HANDOFF.md` con los siguientes pasos inmediatos.
4. Seguir el protocolo de PR en [`.agents/workflows/autonomous-pr.md`](.agents/workflows/autonomous-pr.md).
