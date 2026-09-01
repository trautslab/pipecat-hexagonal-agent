# 🎯 Caso de Uso: UC-004 - Interacción de Voz desde el Navegador Web (WebSocket)

- **ID:** `UC-004`
- **Dominio:** Web / Audio Streaming
- **Actor Principal:** Usuario en Navegador Web (Chrome, Safari, Firefox, Edge)
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-002`](../diagrams/sequences/SEQ-002-websocket-client-streaming.md)
- **Contrato de Tarea:** [`TASK-004`](../../.agents/tasks/TASK-004-web-interface-websocket.md)

---

## 📖 Descripción
El usuario abre la aplicación web desde su navegador. Hace clic en "Iniciar Conversación" y otorga permisos de micrófono. El frontend captura el audio PCM a 16kHz mediante la `Web Audio API`, renderiza una animación de ondas en tiempo real (*Waveform*) en un elemento `<canvas>` y envía el stream por WebSocket al backend. El agente procesa la voz y devuelve las tramas sintetizadas en tiempo real para ser reproducidas en el navegador junto con subtítulos en vivo.

---

## 📋 Precondiciones
1. El servidor web `web_server.py` está en ejecución en el puerto asignado (ej. `http://localhost:8765`).
2. El navegador tiene soporte para `AudioContext` y `WebSocket`.

---

## 🔄 Flujo Principal (Happy Path)
1. El usuario accede a la interfaz web y pulsa el botón de micrófono.
2. El navegador establece una conexión WebSocket persistente `/ws` con el servidor.
3. El usuario habla: el canvas reacciona visualmente a la amplitud de la voz y envía fragmentos PCM.
4. El `WebSocketTransportAdapter` alimenta el pipeline de Pipecat con `AudioRawFrames`.
5. El agente genera la respuesta por streaming y devuelve los frames de audio y texto por el WebSocket.
6. El cliente web reproduce el audio de respuesta y renderiza los subtítulos del asistente.
