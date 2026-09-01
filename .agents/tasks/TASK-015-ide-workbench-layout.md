# 📋 Contrato de Tarea: TASK-015 - Rediseño de Layout Postman / Modern IDE Workbench

- **ID de Tarea:** `TASK-015`
- **Caso de Uso:** [`UC-013`](../../docs/use-cases/UC-013-ide-workbench-layout.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Reestructurar el frontend (`index.html`, `styles.css`, `app.js`) en las 5 zonas visuales de la captura de pantalla: Header, Sidebar, Workbench (con pestañas y panel de respuesta), Right Sidebar (Telemetría ReAct) y Footer.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Renderizado y navegación en Layout IDE Workbench
  Given la interfaz cargada en el navegador
  Then se visualizan las 5 zonas: Header, Sidebar, Workbench, Right Sidebar y Footer
  And el Workbench cuenta con pestañas de sesión y panel inferior de respuesta
  And el visualizador de ondas y el chat interactúan con el WebSocket en tiempo real
```
