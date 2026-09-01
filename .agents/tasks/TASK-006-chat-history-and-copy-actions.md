# 📋 Contrato de Tarea: TASK-006 - Historial de Conversaciones y Acciones de Copiado

- **ID de Tarea:** `TASK-006`
- **Caso de Uso:** [`UC-006`](../../docs/use-cases/UC-006-chat-persistence-and-mcp-scaffolding.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en el cliente web el sidebar de historial de conversaciones estilo ChatGPT / Claude UI, soporte para "+ Nueva Conversación", persistencia en `localStorage`, y botón de copiado 📋 con feedback visual en cada burbuja.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Copiado de mensaje con 1 clic
  Given un mensaje del usuario o del asistente en pantalla
  When el usuario hace clic en el icono 📋
  Then el texto del mensaje se copia en el portapapeles del sistema operativo
  And se muestra la notificación temporal "¡Copiado!"

Scenario: Creación y alternancia de conversaciones
  Given la interfaz web abierta
  When el usuario hace clic en "+ Nueva Conversación"
  Then se inicia una sesión limpia con nuevo session_id
  And la conversación anterior permanece guardada en la lista del sidebar
```
