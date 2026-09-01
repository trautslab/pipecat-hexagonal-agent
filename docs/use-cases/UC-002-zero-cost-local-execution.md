# 🎯 Caso de Uso: UC-002 - Ejecución Local Offline y Gratuita (Zero-Cost)

- **ID:** `UC-002`
- **Dominio:** Local AI / Hardware
- **Actor Principal:** Desarrollador / Usuario Final
- **Estado:** `APPROVED`

---

## 📖 Descripción
El usuario inicia el agente en una máquina sin conexión a servicios de pago en la nube. El sistema utiliza Faster-Whisper, Ollama (Llama 3 / Mistral) y Piper/Kokoro junto con el micrófono y parlante locales, funcionando a costo $0.

---

## 📋 Criterios de Aceptación
1. No se requiere ninguna clave API externa.
2. El sistema arranca con `STT_PROVIDER=whisper_local`, `LLM_PROVIDER=ollama`, `TTS_PROVIDER=piper_local`, `TRANSPORT_PROVIDER=local_audio`.
3. Toda la inferencia y procesamiento de audio ocurren en memoria y CPU/GPU local.
