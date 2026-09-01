# 📋 Contrato de Tarea: TASK-009 - Gestor Dinámico de Servidores MCP

- **ID de Tarea:** `TASK-009`
- **Caso de Uso:** [`UC-007`](../../docs/use-cases/UC-007-openclaw-autonomous-reasoning-mcp.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en `adapters/tools/mcp_manager_adapter.py` la capacidad de registrar servidores MCP en `.agents/mcp/mcp-servers.json` y declarar plantillas de variables de credenciales en `.env`.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Registro dinámico de Google Calendar MCP
  Given el MCPManagerAdapter activo
  When se solicita registrar el servidor "google-calendar" con paquete "@modelcontextprotocol/server-google-calendar"
  Then .agents/mcp/mcp-servers.json se actualiza con la entrada del servidor
  And .env se enriquece con las claves requeridas (GOOGLE_CALENDAR_CLIENT_ID, etc.)
  And retorna la confirmación de configuración
```
