# 🏛️ Architecture Decision Record: ADR-0008 - Consola Lateral Derecha de Trazabilidad en Tiempo Real

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-009`](../use-cases/UC-009-realtime-telemetry-console-sidebar.md)

---

## 1. Contexto y Problema
En la versión previa (`v0.7.0`), la traza técnica se mostraba dentro de la misma burbuja del chat del bot únicamente cuando este ya había terminado de generar su respuesta. Esto generaba dos problemas:
1. Saturaba visualmente el flujo conversacional principal del chat.
2. No reflejaba la naturaleza en tiempo real de los pensamientos y acciones que ocurrían antes y durante la llamada al LLM.

---

## 2. Decisión
1. **Layout de 3 Columnas:** Separar las responsabilidades visuales:
   - **Columna Izquierda:** Historial de sesiones y conversaciones previas.
   - **Columna Central:** Interacción de voz en vivo, canvas reactivo y flujo de chat limpio con numeración correlativa (`#1`, `#2`, `#3`).
   - **Columna Derecha (Right Sidebar Console):** Consola de telemetría en tiempo real con acordeones por cada turno correlativo.
2. **Protocolo WebSocket `live_trace`:** El servidor emite tramas en vivo por cada paso de pensamiento/acción en cuanto se ejecuta, sin esperar la culminación del turno.
3. **Copiado Integral de Consola:** Botón para copiar toda la sesión técnica formateada en Markdown.

---

## 3. Consecuencias
- Experiencia de usuario profesional y limpia (similar a DevTools o paneles de agentes como Devin/OpenHands).
- Visibilidad instantánea de lo que el agente piensa o ejecuta mientras busca en internet o instala herramientas MCP.
