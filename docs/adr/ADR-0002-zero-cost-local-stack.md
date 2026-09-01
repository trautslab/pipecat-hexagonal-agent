# 🏛️ Architecture Decision Record: ADR-0002 - Selección de la Pila Local Gratuita (Zero-Cost Stack)

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-002`](../use-cases/UC-002-zero-cost-local-execution.md)

---

## 1. Contexto y Problema
Se requiere que cualquier desarrollador pueda clonar el repositorio y ejecutar el agente de voz en su propia máquina (ej. Mac Apple Silicon o PC con CPU/GPU moderna) sin costo alguno y sin solicitar tarjetas de crédito ni suscripciones a APIs comerciales.

---

## 2. Decisión
Seleccionar la siguiente combinación de tecnologías locales de código abierto:
1. **STT:** **Faster-Whisper** por su alto rendimiento y optimización con CTranslate2 / CPU / Metal.
2. **LLM:** **Ollama** con endpoint OpenAI-compatible (`http://localhost:11434/v1`) y soporte de streaming token a token para modelos como `llama3.2:3b`.
3. **TTS:** **Piper TTS** o **Kokoro** para síntesis neural de audio offline de alta velocidad.
4. **Transporte:** **Audio Local (SoundDevice / PortAudio)** para comunicarse directamente por el micrófono y altavoz del sistema.

---

## 3. Consecuencias

### Positivas:
- Costo recurrente $0.00.
- Privacidad total (el audio y las conversaciones nunca salen de la máquina local).
- Baja latencia local sin sobrecarga de red.

### Negativas / Trade-offs:
- Requiere recursos de hardware local (RAM y CPU/GPU).
