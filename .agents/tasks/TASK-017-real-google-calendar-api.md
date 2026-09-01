# 📋 Contrato de Tarea: TASK-017 - Integración Real con Google Calendar API v3 y OAuth2

- **ID de Tarea:** `TASK-017`
- **Caso de Uso:** [`UC-015`](../../docs/use-cases/UC-015-real-google-calendar-api-integration.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar `GoogleCalendarClient` con intercambio de tokens OAuth2, endpoint `/oauth2callback` y creación de eventos reales contra la API de Google Calendar v3 (`googleapis.com/calendar/v3/calendars/primary/events`).

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Generación de URL de autorización OAuth2
  Given las credenciales GOOGLE_CALENDAR_CLIENT_ID en .env
  When el cliente solicita la URL de autorización
  Then GoogleCalendarClient genera un enlace válido de Google OAuth2 con scope calendar.events

Scenario: Inserción de evento real en Google Calendar
  Given un token de acceso válido en .agents/tokens/google_token.json
  When el usuario pide agendar un evento
  Then GoogleCalendarClient envía la petición POST a https://www.googleapis.com/calendar/v3/calendars/primary/events
  And retorna el objeto con el ID del evento y el htmlLink oficial de Google
```
