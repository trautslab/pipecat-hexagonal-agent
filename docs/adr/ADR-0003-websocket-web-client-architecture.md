# 🏛️ Architecture Decision Record: ADR-0003 - Arquitectura de Transporte WebSocket para Cliente Web

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-004`](../use-cases/UC-004-web-browser-voice-interaction.md)

---

## 1. Contexto y Problema
Para habilitar una experiencia de usuario interactiva directamente en navegadores web sin requerir infraestructura externa de servidores WebRTC ni cuentas cloud en Daily.co, se requiere un mecanismo de transporte ligero y bidireccional que funcione 100% en local y sea fácilmente integrable con la arquitectura hexagonal existente.

---

## 2. Decisión
1. Implementar un nuevo adaptador `WebSocketTransportAdapter` que cumpla con `TransportPort`.
2. Utilizar WebSockets binarios para transmitir tramas de audio PCM de baja latencia entre el navegador y el pipeline de Pipecat.
3. Construir una interfaz web ligera con `Web Audio API` y renderizado de ondas en `<canvas>` con estética *Dark Mode / Glassmorphism*.

---

## 3. Consecuencias

### Positivas:
- Cero dependencias de servicios WebRTC externos para el cliente web.
- Funciona directamente en `localhost` o en cualquier servidor con soporte HTTP/WS.
- Totalmente compatible con la arquitectura hexagonal sin alterar el Core.

### Negativas / Trade-offs:
- WebSockets no incluye control de congestión nativo como WebRTC para conexiones móviles de mala calidad (aunque es óptimo para local y redes estables).
