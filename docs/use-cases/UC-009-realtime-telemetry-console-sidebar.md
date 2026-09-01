# 🎯 Caso de Uso: UC-009 - Consola Lateral Derecha de Trazabilidad en Tiempo Real y Numeración Correlativa

- **ID:** `UC-009`
- **Dominio:** UI / Observability / Real-Time Telemetry
- **Actor Principal:** Usuario / Ingeniero de Software
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-007`](../diagrams/sequences/SEQ-007-realtime-trace-streaming.md)
- **Contrato de Tarea:** [`TASK-011`](../../.agents/tasks/TASK-011-realtime-console-right-sidebar.md)

---

## 📖 Descripción
El sistema proporciona una **Consola de Trazabilidad Lateral Derecha (Right Sidebar)** dedicada y colapsable, desacoplada visualmente de las burbujas del chat principal.

### Capacidades Principales:
1. **Streaming en Tiempo Real:** Los pasos de razonamiento ReAct (pensamientos, llamadas a herramientas web/MCP, lecturas y modificaciones de archivos) se transmiten inmediatamente por WebSocket conforme se producen en el backend, antes de que el modelo termine de generar su respuesta final.
2. **Numeración Correlativa por Turnos:** Cada mensaje del chat posee un identificador correlativo (`#1`, `#2`, `#3`, etc.), y en la consola derecha existe un acordeón correspondiente a cada turno conversacional.
3. **Copiado de Consola en 1 Clic:** Un botón global `[📋 Copiar Consola]` permite serializar en Markdown toda la telemetría acumulada de la sesión para facilitar el reporte de feedback o depuración.
