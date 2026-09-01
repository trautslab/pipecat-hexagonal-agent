# 🏛️ Architecture Decision Record: ADR-0011 - Persistencia de Estado y Telemetría en el Backend

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-012`](../use-cases/UC-012-server-side-session-telemetry-persistence.md)

---

## 1. Contexto y Problema
El uso exclusivo de `localStorage` en el navegador acoplaba el historial conversacional y la trazabilidad al cliente local. Esto impedía compartir estado entre navegadores, dispositivos móviles o sesiones en modo incógnito.

---

## 2. Decisión
1. Definir el puerto abstracto `SessionRepositoryPort` en `core/ports/`.
2. Implementar `FileSessionRepositoryAdapter` en `adapters/persistence/` para almacenar sesiones en archivos JSON en `.agents/sessions/`.
3. Exponer endpoints REST (`/api/sessions`) para lectura, creación y eliminación de sesiones, además de sincronización automática en cada evento WebSocket.

---

## 3. Consecuencias
- Desacoplamiento total del frontend respecto a la persistencia.
- Compatibilidad inmediata con clientes móviles, interfaces web y CLI.
- Resiliencia ante recargas de página o cambios de navegador.
