# 🎯 Caso de Uso: UC-013 - Layout de Workbench Estilo Postman / Modern IDE

- **ID:** `UC-013`
- **Dominio:** Frontend / UI Design / Developer Experience
- **Actor Principal:** Usuario / Desarrollador de Software
- **Estado:** `APPROVED`
- **Diagrama de Secuencia:** [`SEQ-011`](../diagrams/sequences/SEQ-011-ide-workbench-interaction.md)
- **Contrato de Tarea:** [`TASK-015`](../../.agents/tasks/TASK-015-ide-workbench-layout.md)

---

## 📖 Descripción
La interfaz de usuario adopta una estructura de 5 zonas idéntica a los entornos modernos de desarrollo (Postman / IDE Workbench):
1. **Header:** Barra de navegación superior con semáforo macOS (`🔴🟡🟢`), selector de workspace, búsqueda global y switches de tema/conexión.
2. **Sidebar:** Panel izquierdo jerárquico para colecciones de chats, herramientas y servidores MCP.
3. **Workbench:** Panel central con barra de pestañas, visualizador de audio superior y panel de respuesta/timeline inferior con pestañas (`JSON`, `Preview`, `Visualización`).
4. **Right Sidebar:** Panel derecho para consola ReAct en tiempo real y entrada de prompt rápido.
5. **Footer:** Barra inferior con estado de proveedores, terminal y toggles de paneles.
