# Plazos Chile 🇨🇱

Calculadora jurídica open-source para el cómputo de **plazos legales, judiciales y administrativos** en Chile, más **diferencia exacta entre dos fechas**. Incluye una **aplicación web gratuita** (lista para GitHub Pages) y una **Skill para asistentes de IA** (Claude, Codex, Gemini y ChatGPT).

## Qué incluye este repositorio

- `index.html` — Aplicación web autocontenida (optimizada para celular y computador, sin servidores ni dependencias).
- `skill/SKILL.md` — Instrucciones y reglas jurídicas chilenas para agentes de IA.
- `skill/scripts/calcular_plazo.py` — Script en Python (solo librería estándar) para que el agente calcule fechas de forma exacta sin inventar calendarios.
- `LICENSE` — Licencia MIT.

## Reglas jurídicas implementadas

1. **Días hábiles judiciales (Art. 66 CPC / Art. 50 CC):** Lunes a sábado; descuenta domingos y festivos legales.
2. **Días corridos (Art. 50 CC):** Cuentan todos los días calendario.
3. **Días hábiles administrativos (Art. 25 Ley 19.880):** Lunes a viernes; descuenta sábados, domingos y festivos legales.
4. **Meses y años (Art. 48 CC):** De igual fecha a igual fecha (o último día del mes de vencimiento si el día inicial excede al de término).
5. **Feriados y respaldos legales:** Feriados nacionales verificados 2026–2027, cálculo algorítmico 2028+, feriados regionales opcionales (Arica y Parinacota Ley 20.663; Chillán y Chillán Viejo Ley 20.768) y **alerta de feriado bancario del 31 de diciembre** (Ley 21.791 / Art. 38 DFL 3: sin atención bancaria presencial, pero día hábil judicial y administrativo).

## Cómo usar la Skill en IA

- **Claude Code / Codex / Gemini:** Copia la carpeta `skill/` en tu directorio de skills y pide cálculos como *"Calcula 15 días hábiles judiciales desde el 21/11/2026"*. El agente ejecutará `scripts/calcular_plazo.py`.
- **ChatGPT / Proyectos de Claude:** Copia el contenido de `skill/SKILL.md` en las instrucciones de tu GPT personalizado o Proyecto.

> **Aviso:** Herramienta de apoyo referencial. Verifica siempre feriados extraordinarios por ley publicada en el Diario Oficial o resoluciones especiales de cada tribunal.
