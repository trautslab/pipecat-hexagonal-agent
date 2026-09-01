#!/usr/bin/env bash
set -euo pipefail

# Demo Live Script (AI-SDLC Standard)
# Permite realizar un chequeo y demostración interactiva de los componentes del agente

echo "================================================================="
echo "🎤 PIPECAT HEXAGONAL AGENT - DEMO & INTEGRITY CHECK"
echo "================================================================="

echo "1. [Linter] Verificando límites de arquitectura hexagonal..."
python3 scripts/validate_architecture.py

echo -e "\n2. [Eval Harness] Ejecutando harness de evaluación de tareas..."
python3 evals/harness.py --all

echo -e "\n3. [Unit Tests] Ejecutando suite de tests unitarios..."
python3 -m unittest discover -s tests

echo -e "\n4. [Telemetría] Registrando demostración exitosa..."
python3 scripts/telemetry_logger.py --phase "DEMO" --task "ALL" --status "SUCCESS" --msg "Live demo checks completed successfully"

echo -e "\n================================================================="
echo "✅ Todos los sistemas e invariantes están verificados y listos."
echo "Para iniciar la conversación con audio en vivo:"
echo "👉 python3 main.py"
echo "================================================================="
