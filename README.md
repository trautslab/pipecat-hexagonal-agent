# Pipecat Voice Agent - Arquitectura Hexagonal

Proyecto modular y desacoplado para agentes de voz en tiempo real con **Pipecat**, diseñado con **Arquitectura Hexagonal (Ports & Adapters)** y gobernanza bajo el marco **[AI-SDLC](https://github.com/trautslab/ai-sdlc-framework)**. Permite intercambiar componentes locales y gratuitos (Ollama, Whisper, Piper/Kokoro, Audio local, WebSockets) con servicios cloud (OpenAI, Deepgram, Cartesia, Daily WebRTC) únicamente cambiando variables de entorno.

---

## 🏗️ Arquitectura del Sistema

```
                      ┌────────────────────────────────────────┐
                      │              ADAPTADORES               │
                      │                                        │
                      │  STT: Whisper Local / Deepgram         │
                      │  LLM: Ollama (Llama 3) / OpenAI        │
                      │  TTS: Piper (Local) / Cartesia         │
                      │  Transporte: Audio Local / WS / Daily  │
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
* **Transporte:** `Audio Local` (Micrófono/Altavoz del sistema) o `WebSocket Streaming` (Interfaz Web)

---

## 📦 Requisitos Previos

1. **Python 3.10+**
2. **Ollama instalado y corriendo** (para la opción gratuita):
   ```bash
   # Descargar Ollama desde https://ollama.com y luego ejecutar:
   ollama run llama3.2:3b
   ```

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

---

## 🏃 Modos de Ejecución

### Modo A: Interfaz Web con Visualizador de Ondas en Tiempo Real
Inicia el servidor web y abre tu navegador:
```bash
python3 web_server.py
```
Abre en tu navegador: **`http://localhost:8765`**

### Modo B: Terminal con Micrófono y Altavoz Local
Inicia el agente directamente por consola:
```bash
python3 main.py
```

### Modo C: Validación Total y Demo (AI-SDLC)
Ejecuta el linter arquitectónico, el eval harness y la suite de tests:
```bash
bash scripts/demo_live.sh
```
