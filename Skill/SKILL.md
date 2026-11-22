---
name: plazos-chile
description: Calcula vencimientos de plazos legales, judiciales y administrativos en Chile (Arts. 48-50 CC, 65-66 CPC, Art. 25 Ley 19.880) y diferencia exacta entre dos fechas, considerando feriados nacionales, regionales y alerta de feriado bancario del 31 de diciembre (Ley 21.791). Úsala cuando el usuario pida calcular un plazo procesal o administrativo chileno o contar días hábiles/corridos entre fechas.
---

# Plazos Chile (Cómputo Jurídico Chileno)

Cuando el usuario solicite calcular el vencimiento de un plazo en Chile o contar días entre dos fechas, **no calcules fechas mentalmente**: ejecuta siempre `scripts/calcular_plazo.py` con Python 3 para obtener el resultado exacto y auditable.

## Reglas jurídicas obligatorias

1. **Días hábiles judiciales (Regla general — Art. 66 CPC y Art. 50 CC):**
   - Cuentan de **lunes a sábado**.
   - Se descuentan **domingos** y **festivos legales**.
   - Inicio por defecto: desde el día siguiente a la notificación/fecha base (Art. 65 CPC).
2. **Días corridos (Art. 50 CC):**
   - Cuentan todos los días calendario (lunes a domingo, incluidos festivos).
3. **Días hábiles administrativos (Art. 25 Ley 19.880 / Sumarios):**
   - Cuentan de **lunes a viernes**.
   - Se descuentan **sábados, domingos y festivos legales**.
4. **Meses y años (Art. 48 CC):**
   - De igual fecha a igual fecha (ej. 14 de mayo + 1 mes = 14 de junio). Si el mes de término tiene menos días (ej. 31 de enero + 1 mes), vence el último día de ese mes.
   - Presets comunes: Abandono del procedimiento civil `6 meses` (Art. 152 CPC); Abandono juicio ejecutivo `3 años` (Art. 153 CPC).
5. **Feriado bancario del 31 de diciembre (Ley N° 21.791 / Art. 38 DFL N° 3):**
   - Los bancos no atienden presencialmente al público, pero **sí es día hábil judicial y administrativo** (solo se exceptúa el pago y protesto de letras de cambio). Si el rango o vencimiento incluye un 31 de diciembre, adviértelo explícitamente.
6. **Feriados regionales opcionales:**
   - Región de Arica y Parinacota: 7 de junio (Ley 20.663).
   - Chillán y Chillán Viejo: 20 de agosto (Ley 20.768).

## Uso del script (`scripts/calcular_plazo.py`)

### Modo 1: Calcular vencimiento (sumar o restar plazo)
python3 scripts/calcular_plazo.py vencimiento --fecha 2026-11-21 --cantidad 15 --unidad dias --regimen habil_judicial --operacion sumar --inicio siguiente

### Modo 2: Diferencia entre dos fechas
python3 scripts/calcular_plazo.py diferencia --inicio 2026-05-14 --fin 2026-11-21

## Formato de respuesta al usuario
Entrega siempre:
1. La **fecha de vencimiento** (con día de la semana) o los **tres conteos** (días corridos, hábiles judiciales L-S y hábiles administrativos L-V + desglose calendario).
2. La **norma aplicada** (ej. Art. 65–66 CPC, Art. 48 CC o Art. 25 Ley 19.880).
3. Los **feriados legales descontados** con su ley de respaldo y, si corresponde, la **alerta de feriado bancario del 31 de diciembre** (Ley 21.791).
