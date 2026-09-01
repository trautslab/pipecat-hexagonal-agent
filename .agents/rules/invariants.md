# 🛡️ Invariantes Arquitectónicos y Límites Inviolables

Estos invariantes son **reglas duras no negociables** para cualquier agente de IA o desarrollador humano. Cualquier PR o commit que viole uno de estos invariantes debe ser rechazado automáticamente.

---

## 1. Aislamiento Hexagonal Puro
- **Dirección de Dependencias:** El directorio `core/` NUNCA debe importar nada de `adapters/`. La comunicación ocurre exclusivamente a través de las interfaces abstractas definidas en `core/ports/`.
- **Independencia del Pipeline:** La clase `VoiceAgentPipelineBuilder` debe aceptar cualquier implementación que cumpla los contratos `STTPort`, `LLMPort`, `TTSPort` y `TransportPort`.

---

## 2. Gestión Segura de Credenciales & Configuración
- **Cero Secretos Hardcodeados:** Ninguna clave API (`OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `CARTESIA_API_KEY`, `DAILY_TOKEN`) debe escribirse en código.
- **Tipado Fuerte:** Todo acceso a variables de entorno debe realizarse a través de `config/settings.py` con validación de tipo y valores por defecto seguros.

---

## 3. Experiencia Conversacional & Latencia
- **Manejo de Interrupciones (*Barge-in*):** El pipeline debe tener habilitado `allow_interruptions=True` para cancelar la salida de voz si el usuario empieza a hablar.
- **Garantía de Modo Gratuito / Local:** Todo cambio debe mantener la capacidad de arrancar el agente en modo 100% offline y gratuito con Ollama, Whisper y Piper sin necesidad de conexión a internet o claves API de pago.

---

## 4. Calidad y Cobertura de Tests
- **No Test, No Merge:** Cualquier nuevo adaptador o cambio en el pipeline debe acompañarse de sus pruebas unitarias o mocks correspondientes.
- **Prohibido Relajar Aserciones:** Los tests reflejan el contrato de negocio. Si un test falla tras un cambio, se debe corregir el código o actualizar el contrato si el RFC lo estipula.
