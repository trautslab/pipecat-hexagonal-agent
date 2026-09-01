# 🎯 Caso de Uso: UC-015 - Integración Real con Google Calendar API v3 y Flujo OAuth2

- **ID:** `UC-015`
- **Dominio:** Google Cloud / OAuth2 / Calendar API v3
- **Actor Principal:** Usuario / Google Cloud / Agente Aura
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-013`](../diagrams/sequences/SEQ-013-real-google-oauth-and-event-insertion.md)
- **Contrato de Tarea:** [`TASK-017`](../../.agents/tasks/TASK-017-real-google-calendar-api.md)

---

## 📖 Descripción
El agente se conecta directamente con los endpoints oficiales de Google APIs (`https://www.googleapis.com/calendar/v3/calendars/primary/events`):
1. **Flujo OAuth2:** Utiliza `GOOGLE_CALENDAR_CLIENT_ID` y `GOOGLE_CALENDAR_CLIENT_SECRET` desde `.env`.
2. **Consentimiento:** Ofrece una URL de autorización oficial (`https://accounts.google.com/o/oauth2/v2/auth`) para conceder permisos de escritura en Google Calendar.
3. **Intercambio y Guardado de Tokens:** Captura el código en `http://localhost:8765/oauth2callback`, obtiene el `refresh_token` y lo almacena de forma segura en `.agents/tokens/google_token.json`.
4. **Inserción Real:** Envía una petición `POST` autenticada con Bearer token a la API v3 de Google Calendar, creando físicamente el evento en la nube de Google y retornando el enlace `htmlLink` oficial.
