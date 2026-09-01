# 📋 Contrato de Tarea: TASK-004 - Interfaz Web Interactiva y Adaptador WebSocket

- **ID de Tarea:** `TASK-004`
- **Caso de Uso Relacionado:** [`UC-004`](../../docs/use-cases/UC-004-web-browser-voice-interaction.md)
- **Especificación Técnica:** [`SPEC-001`](../../docs/specs/SPEC-001-voice-agent-contract.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar el adaptador `WebSocketTransportAdapter`, el servidor web asíncrono `web_server.py` y la interfaz web en `web/` con visualizador de ondas de audio en tiempo real y subtítulos en vivo.

---

## 📐 Criterios de Aceptación (BDD / Gherkin)

```gherkin
Scenario: Interacción de voz bidireccional vía WebSocket
  Given el servidor web ejecutándose en el puerto 8765
  And un cliente web conectado al endpoint /ws
  When el cliente transmite tramas de audio PCM desde el micrófono
  Then el WebSocketTransportAdapter inyecta el audio al Core Pipeline
  And el cliente web recibe la respuesta de voz y los eventos de transcripción en streaming
```

---

## 🧪 Comando de Evaluación (Eval Command)
```bash
python3 evals/harness.py --task TASK-004
```
