# 🏛️ Architecture Decision Record: ADR-0010 - Runtime Autónomo de MCPs y Prohibición de Comandos Manuales

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-011`](../use-cases/UC-011-autonomous-mcp-execution-engine.md)

---

## 1. Contexto y Problema
Los modelos de lenguaje pueden caer en el patrón conversacional pasivo de sugerir comandos de terminal al usuario (`npm run sync-google-calendar`, `revisa los logs en...`), lo cual contradice la naturaleza de un agente de ingeniería autónomo como OpenClaw o Devin.

---

## 2. Decisión
1. Implementar `MCPRuntimePort` y `MCPRuntimeAdapter` con capacidad de ejecutar directamente los subprocesos de herramientas MCP, inyectando las variables de entorno de `.env`.
2. Restringir a nivel de System Prompt y formateo ReAct cualquier instrucción manual de terminal dirigida al usuario.
3. El agente asume el 100% de la responsabilidad de ejecución y reporta únicamente los resultados obtenidos.

---

## 3. Consecuencias
- Experiencia de usuario de agente de voz autónomo de primer nivel (*State-of-the-Art*).
- Eliminación total de fricción operativa y de comandos manuales en la terminal.
