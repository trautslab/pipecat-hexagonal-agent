# 🏛️ Architecture Decision Record: ADR-0017 - Discriminación Multi-Acción de Herramientas y Consulta en Vivo de Google Calendar

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-018`](../use-cases/UC-018-calendar-event-query-and-multi-action-tool-calling.md)

---

## 1. Contexto y Problema
Si el usuario envía preguntas de verificación o reclamo (*"no veo lo configurado"*, *"¿estás seguro?"*), el agente no debe intentar crear un evento inventado, sino invocar `google_calendar.list_events` para inspeccionar el estado real de la cuenta de Google Calendar y responder con la verdad.

---

## 2. Decisión
1. Incorporar `list_real_events` y `delete_real_event` a `GoogleCalendarClient` y `MCPRuntimePort`.
2. Segmentar los disparadores de intención en tres categorías ortogonales:
   - **CREACIÓN:** Requiere verbos imperativos (`crea`, `agenda`, `programa`, `quiero que me hagas un evento de...`).
   - **CONSULTA:** Verbos o preguntas de verificación (`no veo`, `estás seguro`, `qué eventos tengo`, `revisa`, `busca el evento`).
   - **ELIMINACIÓN:** Órdenes de borrado (`elimina`, `borra`, `cancela el evento`).
3. Si la intención es consulta, llamar a `list_real_events` y presentar al usuario la lista oficial devuelta por Google APIs.

---

## 3. Consecuencias
- Cero falsos positivos de creación y cero alucinaciones de eventos ficticios.
- Capacidad de auditoría y verificación en tiempo real de los eventos en Google Calendar.
