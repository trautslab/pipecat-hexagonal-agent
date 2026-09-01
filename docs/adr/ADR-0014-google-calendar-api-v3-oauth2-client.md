# 🏛️ Architecture Decision Record: ADR-0014 - Cliente Nativo de Google Calendar API v3 y OAuth2

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-015`](../use-cases/UC-015-real-google-calendar-api-integration.md)

---

## 1. Contexto y Problema
Para que los eventos creados por el asistente se reflejen realmente en el calendario personal del usuario en Google Cloud, es necesario implementar la autenticación OAuth2 y llamadas REST a la API oficial de Google Calendar v3.

---

## 2. Decisión
1. Implementar `GoogleCalendarClient` en `adapters/tools/google_calendar_client.py` utilizando la biblioteca estándar de Python (`urllib.request`, `urllib.parse`, `json`) para evitar dependencias pesadas.
2. Manejar el flujo de intercambio de códigos y refresco de tokens OAuth2 almacenando las credenciales en `.agents/tokens/google_token.json`.
3. Exponer el endpoint `/oauth2callback` en `web_server.py` para completar el ciclo de autorización en el navegador con un solo clic.

---

## 3. Consecuencias
- Los eventos se registran físicamente en el Google Calendar real del usuario.
- Cero dependencias adicionales de terceros (arquitectura ligera y limpia).
- Experiencia de autorización guiada y transparente en la interfaz web.
