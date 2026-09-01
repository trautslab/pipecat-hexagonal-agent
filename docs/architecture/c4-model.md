# 🏛️ Modelo C4: Arquitectura del Sistema de Agente de Voz

Este documento detalla la arquitectura del agente de voz en los niveles de **Contexto**, **Contenedor** y **Componente** según el modelo C4.

---

## Nivel 1: Diagrama de Contexto del Sistema

```mermaid
C4Context
    title Diagrama de Contexto del Sistema - Agente de Voz Pipecat

    Person(user, "Usuario / Interlocutor", "Interactúa por voz con el agente en tiempo real.")
    
    System(voice_agent_system, "Sistema Agente de Voz Hexagonal", "Orquesta STT, LLM, TTS y Transporte para mantener una conversación hablada fluida con ultra-baja latencia.")
    
    System_Ext(ollama, "Ollama Local (LLM)", "Motor de inferencia local para modelos abiertos (Llama 3, Mistral).")
    System_Ext(whisper, "Faster-Whisper (STT)", "Motor local de reconocimiento de voz.")
    System_Ext(piper, "Piper / Kokoro (TTS)", "Sintetizador neuronal de voz local.")
    System_Ext(cloud_services, "Servicios Cloud (OpenAI, Deepgram, Cartesia, Daily)", "Proveedores cloud opcionales para escalabilidad en producción.")

    Rel(user, voice_agent_system, "Habla y escucha", "Audio PCM / WebRTC")
    Rel(voice_agent_system, ollama, "Envía contexto y recibe tokens", "HTTP / Streaming")
    Rel(voice_agent_system, whisper, "Envía tramas de audio y recibe texto", "Memoria / C++ Binding")
    Rel(voice_agent_system, piper, "Envía texto y recibe audio", "Memoria / ONNX")
    Rel(voice_agent_system, cloud_services, "Consumo de APIs REST / WebSockets / WebRTC", "HTTPS / WSS")
```

---

## Nivel 2: Diagrama de Contenedores

```mermaid
C4Container
    title Diagrama de Contenedores - Agente de Voz Pipecat

    Container(app_runtime, "Python Agent Runtime", "Python 3.11+", "Ejecuta el pipeline de Pipecat, el bucle de eventos asyncio y la inyección de dependencias.")
    
    ContainerDb(session_state, "In-Memory Session Context", "Python Dataclasses", "Almacena los turnos de conversación, métricas de latencia y estado.")
    
    Container_Ext(local_hardware, "Dispositivos de Audio", "Micrófono y Parlantes", "Captura y reproduce ondas de sonido a 16kHz.")

    Rel(local_hardware, app_runtime, "Flujo de Audio Entrada", "SoundDevice / PortAudio")
    Rel(app_runtime, local_hardware, "Flujo de Audio Salida", "SoundDevice / PortAudio")
    Rel(app_runtime, session_state, "Lectura / Escritura de historial", "Memoria")
```

---

## Nivel 3: Diagrama de Componentes (Hexagonal)

```mermaid
C4Component
    title Diagrama de Componentes - Capa Core y Adaptadores

    Component(pipeline_builder, "VoiceAgentPipelineBuilder", "Python/Core", "Construye el pipeline de Pipecat conectando los puertos abstractos.")
    Component(ports, "Puertos (STT, LLM, TTS, Transport)", "Python/ABC", "Interfaces abstractas que blindan el núcleo de dependencias externas.")
    Component(factory, "AgentFactory", "Python/Factory", "Resuelve la configuración y conecta los adaptadores concretos a los puertos.")
    Component(adapters_local, "Adaptadores Locales ($0)", "Python/Adapters", "WhisperLocal, Ollama, PiperTTS, LocalAudio.")
    Component(adapters_cloud, "Adaptadores Cloud", "Python/Adapters", "Deepgram, OpenAI, Cartesia, DailyWebRTC.")

    Rel(factory, ports, "Implementa contratos")
    Rel(factory, adapters_local, "Instancia según .env")
    Rel(factory, adapters_cloud, "Instancia según .env")
    Rel(pipeline_builder, ports, "Consume únicamente")
```
