# 🎯 Caso de Uso: UC-016 - Extracción Avanzada de Eventos por Lenguaje Natural

- **ID:** `UC-016`
- **Dominio:** NLP / Semantic Parameter Extraction / Google Calendar
- **Actor Principal:** Usuario / Agente Aura
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-014`](../diagrams/sequences/SEQ-014-nlp-calendar-parameter-extraction.md)
- **Contrato de Tarea:** [`TASK-018`](../../.agents/tasks/TASK-018-natural-language-calendar-extraction.md)

---

## 📖 Descripción
El usuario expresa solicitudes conversacionales complejas de agendamiento como:
> *"Quiero que me hagas un evento para las 5:15 de la tarde del 1 de septiembre del 2026 el evento llámalo preparación para ir al cine Planet de 2 de mayo"*

El sistema debe:
1. **Extraer el Título Exacto:** Identificar cláusulas de nombrado (`llámalo`, `titulado`, `evento llamado`, `con el nombre`) y extraer `Preparación para ir al cine Planet de 2 de mayo`.
2. **Extraer Fecha Completa:** Reconocer patrones como `1 de septiembre del 2026` y mapearlos a `2026-09-01`.
3. **Extraer Hora con Modificador:** Identificar `5:15 de la tarde` y convertir a formato 24 horas (`17:15:00`).
4. **Extraer Ubicación:** Detectar `cine Planet de 2 de mayo` y registrarlo en el campo `location` de Google Calendar.
5. **Generar Descripción Enriquecida y Amable:** Crear un recordatorio personalizado con detalles del evento, emojis y buenos deseos.
