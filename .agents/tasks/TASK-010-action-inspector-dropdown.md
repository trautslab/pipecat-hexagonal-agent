# 📋 Contrato de Tarea: TASK-010 - Inspector Desplegable de Acciones y Telemetría

- **ID de Tarea:** `TASK-010`
- **Caso de Uso:** [`UC-008`](../../docs/use-cases/UC-008-action-inspector-telemetry.md)
- **Estado:** `DONE`
- **Fecha:** 2026-09-01

---

## 🎯 Objetivo de la Tarea
Implementar en el cliente web y servidor el inspector desplegable de acciones (`ActionInspector`) con detalle de operaciones realizadas y botón dedicado de copiado al portapapeles.

---

## 📐 Criterios de Aceptación (BDD)

```gherkin
Scenario: Inspección de acciones y copiado de registro
  Given una respuesta del asistente con acciones ReAct ejecutadas
  When el usuario observa la burbuja de Aura
  Then se muestra el desplegable colapsable "⚡ Acciones y Telemetría Ejecutada ([N] eventos)"
  And al hacer clic en "[📋 Copiar Registro]" se copia la traza estructurada con timestamps y detalles al portapapeles
```
