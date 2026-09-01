# 🏛️ Architecture Decision Record: ADR-0009 - Ejecución Activa y Verificación de Herramientas MCP

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-010`](../use-cases/UC-010-mcp-active-tool-execution.md)

---

## 1. Contexto y Problema
Una vez que el sistema registra los paquetes MCP en `.agents/mcp/mcp-servers.json` y el usuario ingresa sus credenciales en `.env`, el agente necesita ser capaz de ejecutar activamente herramientas (ej. agendar eventos, listar calendarios, ejecutar queries) y comprobar el estado de autenticación, en lugar de solicitar configuraciones manuales irrelevantes.

---

## 2. Decisión
1. Definir el puerto abstracto `MCPExecutorPort` en la capa de puertos del Core.
2. Implementar el adaptador `MCPExecutorAdapter` en `adapters/tools/` con validación de variables de entorno y ejecución de sondas (*probes*) de prueba.
3. Integrar la verificación de credenciales y la ejecución de prueba (evento futuro a 1 minuto) dentro del bucle `AutonomousReasoningEngine`.

---

## 3. Consecuencias
- Cero alucinaciones al interactuar con MCPs ya configurados.
- Ejecución proactiva de acciones reales en Google Calendar y otros servidores MCP.
- Trazabilidad en tiempo real visible en la Consola Lateral Derecha.
