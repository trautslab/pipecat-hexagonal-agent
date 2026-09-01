# 🤝 Guía de Contribución al Proyecto

Gracias por contribuir a `pipecat-hexagonal-agent`. Este proyecto sigue estrictamente el marco de desarrollo **AI-SDLC**.

---

## 1. Convención de Commits (Conventional Commits)

Los mensajes de commit deben seguir la estructura:
`<tipo>(<ámbito opcional>): <descripción>`

Ejemplos:
- `feat(stt): add AssemblyAI adapter support`
- `fix(pipeline): resolve audio frame drop on barge-in`
- `docs(adr): add ADR-0003 for multimodal vision stream`
- `test(core): add edge cases for empty audio frames`

---

## 2. Invariantes No Negociables

Antes de crear un Pull Request o solicitar merge:
1. Ningún archivo en `core/` debe importar código de `adapters/`.
2. Todos los tests deben pasar:
   ```bash
   python3 -m unittest discover -s tests
   python3 scripts/validate_architecture.py
   python3 evals/harness.py --all
   ```
3. La documentación de casos de uso y diagramas debe actualizarse si se añade una nueva funcionalidad.
