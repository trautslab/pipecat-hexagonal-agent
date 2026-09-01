# 🏛️ Architecture Decision Record: ADR-0015 - Extracción de Metadatos de Calendario y Generación de Descripciones Amables

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-016`](../use-cases/UC-016-natural-language-event-extraction.md)

---

## 1. Contexto y Problema
El motor anterior asignaba títulos genéricos y descripciones estáticas en lugar de interpretar los matices conversacionales (título nombrado, fecha explícita, modificadores de tarde/noche y detalles de recordatorio).

---

## 2. Decisión
1. Incorporar un analizador léxico y semántico modular en `AutonomousReasoningEngine` que extraiga:
   - Título explícito (`llámalo...`, `titulado...`, o frase del evento).
   - Fecha completa en lenguaje natural (`1 de septiembre del 2026` -> ISO date).
   - Hora normalizada en formato 24h con modificadores (*de la tarde* -> +12h).
   - Ubicación si es mencionada en el contexto.
2. Generar automáticamente un cuerpo de descripción amable y estructurado con emojis y recordatorios útiles.
3. Extender `GoogleCalendarClient.insert_real_event()` para admitir `description`, `location`, `date` y `time`.

---

## 3. Consecuencias
- Los eventos en Google Calendar reflejan con fidelidad milimétrica lo que el usuario habló.
- La experiencia del usuario es cálida, profesional y detallada.
