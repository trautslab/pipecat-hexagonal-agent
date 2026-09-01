# 🏛️ Architecture Decision Record: ADR-0018 - Enrutamiento Exhaustivo de Verbos de Recordatorio y Corrección de Heurística de Grounding

- **Estado:** `ACCEPTED`
- **Fecha:** 2026-09-01
- **Decisores:** Ingeniero de Software Principal
- **Caso de Uso:** [`UC-019`](../use-cases/UC-019-reminder-synonym-routing-and-grounding-isolation.md)

---

## 1. Contexto y Problema
En `GroundingService`, la condición `len(user_text.split()) >= 4` interceptaba de forma agresiva cualquier frase de más de 3 palabras, enviándola a búsqueda web DuckDuckGo en lugar de ejecutar Google Calendar. Asimismo, frases con verbos coloquiales como *"hazme recordar"*, *"agendes"*, *"avísame"* no estaban incluidas en el vocabulario de intenciones de calendario.

---

## 2. Decisión
1. **Eliminar la regla genérica de conteo de palabras en `GroundingService`**: La búsqueda web solo se ejecutará cuando existan términos explícitos de consulta factual o de internet (`dónde queda`, `quién es`, `noticias de`, `busca en internet`).
2. **Ampliar el catálogo de verbos y tiempos gramaticales en `classify_calendar_intent`**:
   - Recordatorios: `hazme recordar`, `recuérdame`, `recuerdame`, `avísame`, `recordatorio para`.
   - Subjuntivos e imperativos: `agendes`, `agendame`, `agéndame`, `crees`, `creame`, `créame`, `pongas`, `ponme`, `registres`, `registrame`.
   - Modificadores temporales: `hoy día`, `10 de la noche`, `10 pm`, etc.

---

## 3. Consecuencias
- Eliminación total de falsos negativos hacia búsqueda web.
- Procesamiento fluido y natural de recordatorios cotidianos (*descongelar el pollo*, *reuniones*, *citas*).
