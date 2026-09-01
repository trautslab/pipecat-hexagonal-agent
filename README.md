# Pipecat Voice Agent - Arquitectura Hexagonal

Proyecto modular y desacoplado para agentes de voz en tiempo real con **Pipecat**, diseñado con **Arquitectura Hexagonal (Ports & Adapters)**. Permite intercambiar componentes locales y gratuitos (Ollama, Whisper, Piper/Kokoro, Audio local) con servicios cloud (OpenAI, Deepgram, Cartesia, Daily WebRTC) únicamente cambiando variables de entorno.

---

## 🏗️ Arquitectura del Sistema

```
                      ┌────────────────────────────────────────┐
                      │              ADAPTADORES               │
                      │                                        │
                      │  STT: Whisper Local / Deepgram         │
                      │  LLM: Ollama (Llama 3) / OpenAI        │
                      │  TTS: Piper (Local) / Cartesia         │
                      │  Transporte: Audio Local / Daily       │
                      └───────────────────┬────────────────────┘
                                          │ Implementan
                                          ▼
                      ┌────────────────────────────────────────┐
                      │                PUERTOS                 │
                      │  • STTPort      • LLMPort              │
                      │  • TTSPort      • TransportPort        │
                      └───────────────────┬────────────────────┘
                                          │ Inyectados en
                                          ▼
                      ┌────────────────────────────────────────┐
                      │             DOMINIO / CORE             │
                      │  • VoiceAgentPipelineBuilder           │
                      │  • Gestor de Contexto Conversacional   │
                      │  • Manejo de Interrupciones (Barge-in) │
                      └────────────────────────────────────────┘
```

---

## 🚀 Pila 100% Gratuita (Zero-Cost Stack)

* **STT (Speech-to-Text):** `Faster-Whisper` / `Whisper Local` (Corre local en CPU / Apple Silicon)
* **LLM (Language Model):** `Ollama` (con `llama3.2:3b`, `qwen2.5` o `mistral`)
* **TTS (Text-to-Speech):** `Piper TTS` o `Kokoro` (síntesis de voz rápida local)
* **Transporte:** `Audio Local` (Micrófono y altavoz del sistema mediante SoundDevice/PyAudio)

---

## 📦 Requisitos Previos

1. **Python 3.10+**
2. **Ollama instalado y corriendo** (para la opción gratuita):
   ```bash
   # Descargar Ollama desde https://ollama.com y luego ejecutar:
   ollama run llama3.2:3b
   ```
3. *(Opcional)* Herramientas de audio del sistema (ej. en Mac: `brew install portaudio`)

---

## ⚙️ Instalación y Configuración

1. **Crear entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar el entorno:**
   ```bash
   cp .env.example .env
   ```

Edita `.env` según los proveedores que quieras activar.

---

## 🎛️ Configuración de Proveedores (`.env`)

### Modo 1: 100% Gratuito y Local (Por Defecto)
```env
STT_PROVIDER=whisper_local
LLM_PROVIDER=ollama
TTS_PROVIDER=piper_local
TRANSPORT_PROVIDER=local_audio

# Configuración Ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:3b

# Prompt del Asistente
AGENT_SYSTEM_PROMPT="Eres un asistente de voz inteligente, empático y conciso. Responde en español de forma natural y breve."
```

### Modo 2: Híbrido o Cloud (Intercambiable sin tocar código)
```env
STT_PROVIDER=deepgram
LLM_PROVIDER=openai
TTS_PROVIDER=cartesia
TRANSPORT_PROVIDER=daily_webrtc

# API Keys
DEEPGRAM_API_KEY=tu_clave_deepgram
OPENAI_API_KEY=tu_clave_openai
CARTESIA_API_KEY=tu_clave_cartesia
DAILY_ROOM_URL=https://tu-dominio.daily.co/tu-sala
DAILY_TOKEN=tu_token_daily
```

---

## 🏃 Ejecución

Para iniciar el agente:
```bash
python main.py
```

Habla por tu micrófono y el agente te responderá en tiempo real a través de los altavoces.
