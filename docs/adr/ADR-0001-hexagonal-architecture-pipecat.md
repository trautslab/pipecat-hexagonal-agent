# 🏛️ Architecture Decision Record: ADR-0001 - Adopción de Arquitectura Hexagonal sobre Pipecat

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-001`](../use-cases/UC-001-realtime-voice-conversation.md), [`UC-002`](../use-cases/UC-002-zero-cost-local-execution.md)

---

## 1. Contexto y Problema
El desarrollo de agentes de voz con Inteligencia Artificial suele quedar acoplado a APIs específicas (OpenAI Realtime API, Deepgram, Cartesia, Daily.co). Esto dificulta:
1. El prototipado y ejecución local a costo $0 con modelos Open Source.
2. El reemplazo ágil de proveedores sin romper el orquestador conversacional.
3. La ejecución de pruebas unitarias herméticas sin consumir créditos de red ni depender de micrófonos físicos.

---

## 2. Decisión
Adoptar **Arquitectura Hexagonal (Ports & Adapters)** dividiendo el sistema en:
1. **Core / Dominio:** Contratos de orquestación (`VoiceAgentPipelineBuilder`) y sesión (`AgentSession`).
2. **Puertos:** Interfaces abstractas `STTPort`, `LLMPort`, `TTSPort` y `TransportPort`.
3. **Adaptadores:** Implementaciones aisladas para Whisper, Ollama, Piper, Deepgram, OpenAI, Cartesia, Daily y Mocks.
4. **Factoría:** `AgentFactory` encargada de la inyección de dependencias mediante variables de entorno.

---

## 3. Consecuencias

### Positivas:
- Desacoplamiento total: cambiar de proveedor requiere únicamente cambiar 1 línea en `.env`.
- Pila 100% gratuita ejecutable en modo local offline.
- Capacidad de tests unitarios ultrarrápidos con adaptadores mock.

### Negativas / Trade-offs:
- Pequeña capa adicional de abstracción sobre las clases directas de Pipecat.
