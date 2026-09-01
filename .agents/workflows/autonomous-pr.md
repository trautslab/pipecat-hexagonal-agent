# 🚀 Protocolo de Creación de Pull Request Autónomo

Este flujo es ejecutado por el agente de IA para empaquetar y entregar un conjunto de cambios completo y verificado.

---

## 1. Verificaciones Previas Obligatorias
Antes de generar el commit o PR:
1. `python3 scripts/validate_architecture.py` -> Debe pasar sin violaciones de frontera.
2. `python3 evals/harness.py --all` -> 100% de tareas pasando.
3. `python3 -m unittest discover -s tests` -> 100% tests unitarios pasando.
4. `CHANGELOG.md` -> Sección `[Unreleased]` actualizada con los cambios.
5. `HANDOFF.md` -> Siguientes pasos actualizados.

---

## 2. Estructura del Mensaje de Commit / PR
- **Título:** `feat(hexagonal): complete zero-cost voice agent and AI-SDLC governance`
- **Cuerpo del PR:**
  - 📋 **Resumen de Cambios:** Qué se implementó y por qué.
  - 🛡️ **Invariantes Verificados:** Confirmación de respeto a las reglas no negociables.
  - 🧪 **Resultados de Pruebas:** Salida de los comandos de evaluación.
  - 🗺️ **Documentación Vinculada:** Enlaces a `docs/INDEX.md`, Casos de Uso y ADRs.
