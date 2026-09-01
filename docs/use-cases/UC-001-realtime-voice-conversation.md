# 🎯 Caso de Uso: UC-001 - Conversación de Voz Bidireccional en Tiempo Real

- **ID:** `UC-001`
- **Dominio:** Core / Audio Pipeline
- **Actor Principal:** Usuario (Interlocutor)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-001`](../diagrams/sequences/SEQ-001-voice-streaming-pipeline.md)
- **Diagrama de Actividad:** [`ACT-001`](../diagrams/activities/ACT-001-audio-barge-in-interruption.md)
- **Máquina de Estados:** [`STM-001`](../diagrams/state-machines/STM-001-agent-session-lifecycle.md)

---

## 📖 Descripción
El usuario habla a través de su micrófono. El sistema captura el audio en streaming, lo transcribe a texto en tiempo real, genera una respuesta inteligente mediante un LLM y sintetiza la voz para reproducirla por los altavoces con latencia inferior a 800ms. Si el usuario interrumpe mientras el bot habla, el bot calla de inmediato (*barge-in*).

---

## 📋 Precondiciones
1. El pipeline del agente está inicializado y en estado `LISTENING`.
2. Los puertos STT, LLM, TTS y Transporte están correctamente inyectados.

---

## 🔄 Flujo Principal (Happy Path)
1. El usuario habla diciendo una frase.
2. El `TransportPort` captura los bloques PCM y los envía al `STTPort`.
3. El `STTPort` transcribe la frase y emite un `TextFrame`.
4. El agregador agrupa el turno y el `LLMPort` genera tokens de respuesta en streaming.
5. El `TTSPort` recibe los tokens y empieza a producir fragmentos de audio inmediatamente.
6. El `TransportPort` reproduce el audio en los parlantes.
7. El turno completo se guarda en `AgentSession`.
