# 🎨 Guía de Estilo y Clean Code (Python & Bash)

Estándares obligatorios de codificación para el repositorio.

---

## 1. Estándares en Python

1. **Tipado Estricto (Type Hints):**
   - Todas las funciones y métodos públicos deben tener anotaciones de tipos completas en argumentos y retornos.
   - Uso de `Optional`, `List`, `Dict`, `Any`, `Union` de `typing`.

2. **Manejo Defensivo de Excepciones:**
   - Capturar excepciones específicas siempre que sea posible.
   - Loggear errores con contexto usando `config.logger_config.logger`.

3. **Inmutabilidad y Clases de Datos:**
   - Uso de `@dataclass` para entidades y DTOs de dominio.
   - Métodos explícitos para mutación de estado en entidades de sesión.

---

## 2. Estándares en Scripts Bash

1. **Flags de Seguridad:**
   - Todo script bash debe comenzar con `set -euo pipefail` para frenar en errores o variables no declaradas.
2. **Mensajes Claros:**
   - Salidas estructuradas con colores y prefijos legibles.
