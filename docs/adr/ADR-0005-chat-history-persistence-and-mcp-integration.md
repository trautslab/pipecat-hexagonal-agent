# 🏛️ Architecture Decision Record: ADR-0005 - Persistencia de Conversaciones y Autoconocimiento de MCPs

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-006`](../use-cases/UC-006-chat-persistence-and-mcp-scaffolding.md)

---

## 1. Contexto y Problema
El usuario necesita:
1. Copiar mensajes fácilmente para acelerar su flujo de trabajo.
2. Un asistente que no dé respuestas derrotistas ("no puedo hacer eso"), sino que entienda su propia base de código (`pipecat-hexagonal-agent`), proponga el código y las variables de entorno necesarias para conectar MCPs (ej. Google Calendar) y actúe proactivamente.
3. Poder crear, guardar y reanudar sesiones conversacionales manteniendo el contexto de la conversación (estilo ChatGPT/Claude).

---

## 2. Decisión
1. Implementar en el frontend un gestor de sesiones con persistencia en `localStorage`, lista de chats pasados en un sidebar y botón de copiado por mensaje.
2. Configurar el `AGENT_SYSTEM_PROMPT` con la especificación completa del repositorio (arquitectura hexagonal, puertos, adaptadores, variables `.env`, servidores MCP).
3. En el backend, mantener el historial multi-turno de mensajes para alimentar el contexto de Ollama cuando el usuario reanuda una sesión.

---

## 3. Consecuencias
- Experiencia de usuario de nivel comercial (ChatGPT / Claude UI con voz nativa).
- Capacidad de evolucionar y conectar nuevas herramientas de manera asistida.
