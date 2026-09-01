# 📋 Contrato de Tarea: TASK-001 - Núcleo y Puertos de Arquitectura Hexagonal

- **ID de Tarea:** `TASK-001`
- **Caso de Uso Relacionado:** [`UC-001`](../../docs/use-cases/UC-001-realtime-voice-conversation.md)
- **Especificación Técnica:** [`SPEC-001`](../../docs/specs/SPEC-001-voice-agent-contract.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Definir las interfaces abstractas (`STTPort`, `LLMPort`, `TTSPort`, `TransportPort`) y el constructor agnóstico `VoiceAgentPipelineBuilder` en la capa de dominio `core/`.

---

## 📐 Criterios de Aceptación (BDD / Gherkin)

```gherkin
Scenario: Ensamblaje exitoso de pipeline agnóstico con puertos abstractos
  Given una sesión de agente inicializada con prompt del sistema
  And adaptadores que implementan STTPort, LLMPort, TTSPort y TransportPort
  When el VoiceAgentPipelineBuilder ejecuta build_pipeline()
  Then se genera un Pipeline de Pipecat válido con los 7 procesadores de audio y turnos
  And el núcleo no contiene ninguna importación directa desde el directorio adapters/
```

---

## 🧪 Comando de Evaluación (Eval Command)
```bash
python3 evals/harness.py --task TASK-001
```
