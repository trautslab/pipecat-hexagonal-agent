# 🎯 Caso de Uso: UC-019 - Enrutamiento Robusto de Recordatorios y Aislamiento de Búsqueda Web

- **ID:** `UC-019`
- **Dominio:** Intent Routing / Natural Reminders / Grounding Guard
- **Actor Principal:** Usuario / LLM (Llama 3.1) / GoogleCalendarClient
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-017`](../diagrams/sequences/SEQ-017-reminder-tool-routing.md)
- **Contrato de Tarea:** [`TASK-021`](../../.agents/tasks/TASK-021-reminder-routing-fix.md)

---

## 📖 Descripción
Garantiza que frases naturales como *"hazme recordar hoy a las 10 de la noche que tengo que descongelar el pollo"* o *"quiero que me agendes un registro"* se enruten directamente a Google Calendar sin caer en búsquedas web innecesarias (eliminando la heurística defectuosa de longitud de palabras en `GroundingService`).
