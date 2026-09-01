# 📋 Contrato de Tarea: TASK-003 - Adaptadores Cloud para Producción y Conmutación Híbrida

- **ID de Tarea:** `TASK-003`
- **Caso de Uso Relacionado:** [`UC-003`](../../docs/use-cases/UC-003-cloud-hybrid-switch.md)
- **Especificación Técnica:** [`SPEC-001`](../../docs/specs/SPEC-001-voice-agent-contract.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar los adaptadores cloud de producción intercambiables:
- `DeepgramSTTAdapter` (STT Cloud)
- `OpenAILLMAdapter` (LLM Cloud GPT-4o)
- `CartesiaTTSAdapter` (TTS Cloud Sonic)
- `DailyWebRTCTransportAdapter` (WebRTC Cloud)

---

## 📐 Criterios de Aceptación (BDD / Gherkin)

```gherkin
Scenario: Conmutación a adaptadores Cloud mediante variables de entorno
  Given claves API configuradas en .env (DEEPGRAM_API_KEY, OPENAI_API_KEY, CARTESIA_API_KEY, DAILY_ROOM_URL)
  And los proveedores configurados como deepgram, openai, cartesia, daily_webrtc
  When se ejecuta AgentFactory.build_agent()
  Then el agente se ensambla con los servicios cloud sin alterar una sola línea del core
```

---

## 🧪 Comando de Evaluación (Eval Command)
```bash
python3 evals/harness.py --task TASK-003
```
