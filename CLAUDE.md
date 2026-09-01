# 🛠️ CLAUDE.md - Cheat Sheet de Desarrollo

Comandos rápidos y directrices operativas para asistentes de IA y desarrolladores en `pipecat-hexagonal-agent`.

---

## ⚡ Comandos Esenciales

```bash
# 1. Ejecutar tests unitarios
python3 -m unittest discover -s tests

# 2. Ejecutar Harness de Evaluación Automatizada (AI-SDLC)
python3 evals/harness.py --all

# 3. Validar límites e invariantes de arquitectura hexagonal
python3 scripts/validate_architecture.py

# 4. Registrar evento en telemetría
python3 scripts/telemetry_logger.py --phase "EXECUTION" --task "TASK-001" --status "SUCCESS" --msg "Adapters validated"

# 5. Ejecutar demostración interactiva
bash scripts/demo_live.sh

# 6. Iniciar agente en modo interactivo
python3 main.py
```

---

## 🛡️ Invariantes Clave
- No importar desde `adapters/` dentro de `core/`.
- No alterar tests para esconder fallos; corregir la implementación.
- Variables de entorno siempre tipadas en `config/settings.py`.
