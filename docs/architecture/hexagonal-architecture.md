# 🔷 Arquitectura Hexagonal en Pipecat (Ports & Adapters)

## 1. Motivación y Principios

En aplicaciones de voz con IA en tiempo real, los proveedores de modelos (LLMs, STT, TTS) y plataformas de transporte (WebRTC, SIP, WebSockets) evolucionan a un ritmo acelerado. 

Acoplar la lógica conversacional a una librería específica (como `openai` o `cartesia`) genera deuda técnica y bloquea la capacidad de ejecutar agentes en local sin costos.

La **Arquitectura Hexagonal** resuelve esto aislando el flujo conversacional en el **Dominio (Core)** y exponiendo **Puertos** que son implementados por **Adaptadores** intercambiables.

---

## 2. Mapa de Capas

```
[ CAPA EXTERNA / INFRAESTRUCTURA ]
  ├── STT: Faster-Whisper | Deepgram | AssemblyAI
  ├── LLM: Ollama (Llama 3) | OpenAI (GPT-4o) | Anthropic (Claude)
  ├── TTS: Piper / Kokoro | Cartesia Sonic | ElevenLabs
  └── Transporte: SoundDevice Mic/Spk | Daily WebRTC | WebSockets
                 │
                 ▼
[ CAPA DE PUERTOS / INTERFACES ]
  ├── STTPort (get_service)
  ├── LLMPort (get_service, get_system_prompt)
  ├── TTSPort (get_service)
  └── TransportPort (get_input, get_output, get_transport)
                 │
                 ▼
[ CAPA DE DOMINIO / CORE PIPELINE ]
  ├── VoiceAgentPipelineBuilder (Orquesta frames de audio y turnos)
  ├── AgentSession (Estado e historial de mensajes)
  └── Invariante de Interrupción (Barge-in nativo)
```

---

## 3. Beneficios Comprobados

1. **Intercambio en 1 línea (`.env`):** Cambiar de `LLM_PROVIDER=ollama` a `LLM_PROVIDER=openai` no requiere tocar ni una sola línea de código.
2. **Testabilidad Aislada:** Permite ejecutar tests con `MockAdapters` en milisegundos sin llamadas de red ni hardware de audio real.
3. **Cero Vendor Lock-in:** Libertad total para migrar a nuevos modelos open-source o proveedores cloud según costo y latencia.
