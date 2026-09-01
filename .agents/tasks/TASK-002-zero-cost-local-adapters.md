# 📋 Contrato de Tarea: TASK-002 - Adaptadores Locales 100% Gratuitos (Zero-Cost)

- **ID de Tarea:** `TASK-002`
- **Caso de Uso Relacionado:** [`UC-002`](../../docs/use-cases/UC-002-zero-cost-local-execution.md)
- **Especificación Técnica:** [`SPEC-001`](../../docs/specs/SPEC-001-voice-agent-contract.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar los adaptadores para ejecución local y sin costo en hardware propio:
- `WhisperLocalSTTAdapter` (Faster-Whisper / STT Local)
- `OllamaLLMAdapter` (Ollama Llama 3 / LLM Local)
- `PiperLocalTTSAdapter` (Piper / Kokoro TTS Local)
- `LocalAudioTransportAdapter` (Micrófono y Parlantes locales)

---

## 📐 Criterios de Aceptación (BDD / Gherkin)

```gherkin
Scenario: Inicialización de agente en modo 100% gratuito y offline
  Given la configuración STT_PROVIDER=whisper_local, LLM_PROVIDER=ollama, TTS_PROVIDER=piper_local, TRANSPORT_PROVIDER=local_audio
  When la factoría AgentFactory.build_agent() es invocada
  Then se instancian adaptadores locales sin requerir credenciales API cloud
  And el agente está listo para procesar audio mediante el hardware local
```

---

## 🧪 Comando de Evaluación (Eval Command)
```bash
python3 evals/harness.py --task TASK-002
```
