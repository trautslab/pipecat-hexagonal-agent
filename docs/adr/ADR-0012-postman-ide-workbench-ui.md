# 🏛️ Architecture Decision Record: ADR-0012 - Rediseño de Interfaz a Layout Postman / Modern IDE Workbench

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-013`](../use-cases/UC-013-ide-workbench-layout.md)

---

## 1. Contexto y Problema
Para ofrecer una experiencia de desarrollo de voz e ingeniería de agentes de clase mundial, la interfaz requería organizarse en un layout estructurado de 5 regiones (Header, Sidebar, Workbench con pestañas, Right Sidebar para AI/Telemetría y Footer).

---

## 2. Decisión
1. Implementar la maqueta HTML/CSS estructurada con CSS Grid y Flexbox en 5 zonas:
   - `ide-header` (Top)
   - `ide-sidebar` (Left)
   - `ide-workbench` (Center: tabs, upper audio stage, lower response timeline)
   - `ide-right-sidebar` (Right: real-time console)
   - `ide-footer` (Bottom: status, logs, layout controls)
2. Mantener total compatibilidad con WebSocket, AudioContext, SpeechRecognition, streaming de trazas y persistencia en servidor.

---

## 3. Consecuencias
- Estética y usabilidad de primer nivel comparables a Postman / VSCode.
- Máxima claridad para monitorear ejecuciones de voz y herramientas MCP en simultáneo.
