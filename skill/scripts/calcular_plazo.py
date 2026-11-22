#!/usr/bin/env python3
"""Calculadora jurídica de plazos y diferencia entre fechas para Chile."""

import argparse
import calendar
import datetime as dt
import json

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

VERIFIED_HOLIDAYS = {
    2026: {
        "2026-01-01": ("Año Nuevo", "Ley 2.977 / Ley 19.973"),
        "2026-04-03": ("Viernes Santo", "Ley 2.977"),
        "2026-04-04": ("Sábado Santo", "Ley 2.977"),
        "2026-05-01": ("Día Nacional del Trabajo", "Código del Trabajo / Ley 19.973"),
        "2026-05-21": ("Día de las Glorias Navales", "Ley 2.977"),
        "2026-06-21": ("Día Nacional de los Pueblos Indígenas", "Ley 21.357"),
        "2026-06-29": ("San Pedro y San Pablo", "Ley 2.977 / Ley 18.432 / Ley 19.668"),
        "2026-07-16": ("Día de la Virgen del Carmen", "Ley 20.148"),
        "2026-08-15": ("Asunción de la Virgen", "Ley 2.977"),
        "2026-09-18": ("Independencia Nacional", "Ley 2.977 / Ley 19.973"),
        "2026-09-19": ("Día de las Glorias del Ejército", "Ley 2.977 / Ley 20.629"),
        "2026-10-12": ("Encuentro de Dos Mundos", "Ley 3.810 / Ley 19.668"),
        "2026-10-31": ("Día Nacional de las Iglesias Evangélicas", "Ley 20.299"),
        "2026-11-01": ("Día de Todos los Santos", "Ley 2.977"),
        "2026-12-08": ("Inmaculada Concepción", "Ley 2.977"),
        "2026-12-25": ("Navidad", "Ley 2.977 / Ley 19.973"),
    },
    2027: {
        "2027-01-01": ("Año Nuevo", "Ley 2.977 / Ley 19.973"),
        "2027-03-26": ("Viernes Santo", "Ley 2.977"),
        "2027-03-27": ("Sábado Santo", "Ley 2.977"),
        "2027-05-01": ("Día Nacional del Trabajo", "Código del Trabajo / Ley 19.973"),
        "2027-05-21": ("Día de las Glorias Navales", "Ley 2.977"),
        "2027-06-21": ("Día Nacional de los Pueblos Indígenas", "Ley 21.357"),
        "2027-06-28": ("San Pedro y San Pablo (trasladado)", "Ley 2.977 / Ley 18.432 / Ley 19.668"),
        "2027-07-16": ("Día de la Virgen del Carmen", "Ley 20.148"),
        "2027-08-15": ("Asunción de la Virgen", "Ley 2.977"),
        "2027-09-18": ("Independencia Nacional", "Ley 2.977 / Ley 19.973"),
        "2027-09-19": ("Día de las Glorias del Ejército", "Ley 2.977 / Ley 20.629"),
        "2027-10-11": ("Encuentro de Dos Mundos (trasladado)", "Ley 3.810 / Ley 19.668"),
        "2027-10-30": ("Día Nacional de las Iglesias Evangélicas", "Ley 20.299"),
        "2027-11-01": ("Día de Todos los Santos", "Ley 2.977"),
        "2027-12-08": ("Inmaculada Concepción", "Ley 2.977"),
        "2027-12-25": ("Navidad", "Ley 2.977 / Ley 19.973"),
    },
}


def easter_sunday(year: int) -> dt.date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def shift_monday_ley_19668(d: dt.date) -> dt.date:
    wd = d.weekday()
    if wd in (1, 2, 3):
        return d - dt.timedelta(days=wd)
    if wd == 4:
        return d + dt.timedelta(days=3)
    return d


def holidays_for_year(year: int, regional: str = "ninguno") -> dict:
    if year in VERIFIED_HOLIDAYS:
        h = dict(VERIFIED_HOLIDAYS[year])
    else:
        e = easter_sunday(year)
        h = {
            f"{year}-01-01": ("Año Nuevo", "Ley 2.977 / Ley 19.973"),
            (e - dt.timedelta(days=2)).isoformat(): ("Viernes Santo", "Ley 2.977"),
            (e - dt.timedelta(days=1)).isoformat(): ("Sábado Santo", "Ley 2.977"),
            f"{year}-05-01": ("Día Nacional del Trabajo", "Código del Trabajo / Ley 19.973"),
            f"{year}-05-21": ("Día de las Glorias Navales", "Ley 2.977"),
            f"{year}-06-21": ("Día Nacional de los Pueblos Indígenas", "Ley 21.357"),
            shift_monday_ley_19668(dt.date(year, 6, 29)).isoformat(): ("San Pedro y San Pablo", "Ley 2.977 / Ley 19.668"),
            f"{year}-07-16": ("Día de la Virgen del Carmen", "Ley 20.148"),
            f"{year}-08-15": ("Asunción de la Virgen", "Ley 2.977"),
            f"{year}-09-18": ("Independencia Nacional", "Ley 2.977 / Ley 19.973"),
            f"{year}-09-19": ("Día de las Glorias del Ejército", "Ley 2.977 / Ley 20.629"),
            shift_monday_ley_19668(dt.date(year, 10, 12)).isoformat(): ("Encuentro de Dos Mundos", "Ley 3.810 / Ley 19.668"),
            f"{year}-11-01": ("Día de Todos los Santos", "Ley 2.977"),
            f"{year}-12-08": ("Inmaculada Concepción", "Ley 2.977"),
            f"{year}-12-25": ("Navidad", "Ley 2.977 / Ley 19.973"),
        }
        oct31 = dt.date(year, 10, 31)
        if oct31.weekday() == 1:
            ev = oct31 - dt.timedelta(days=4)
        elif oct31.weekday() == 2:
            ev = oct31 + dt.timedelta(days=2)
        else:
            ev = oct31
        h[ev.isoformat()] = ("Día Nacional de las Iglesias Evangélicas", "Ley 20.299")

    if regional == "arica":
        h[f"{year}-06-07"] = ("Asalto y Toma del Morro de Arica (Regional)", "Ley 20.663")
    elif regional == "chillan":
        h[f"{year}-08-20"] = ("Nacimiento de Bernardo O’Higgins (Chillán / Chillán Viejo)", "Ley 20.768")
    return h


def holiday_info(d: dt.date, regional: str):
    return holidays_for_year(d.year, regional).get(d.isoformat())


def is_inhabil(d: dt.date, regimen: str, regional: str) -> bool:
    wd = d.weekday()
    hol = holiday_info(d, regional) is not None
    if regimen == "habil_judicial":
        return wd == 6 or hol
    if regimen == "habil_admin":
        return wd in (5, 6) or hol
    return False


def add_months_civil(d: dt.date, months: int) -> dt.date:
    total_m = d.year * 12 + (d.month - 1) + months
    y = total_m // 12
    m = (total_m % 12) + 1
    last_day = calendar.monthrange(y, m)[1]
    return dt.date(y, m, min(d.day, last_day))


def fmt_largo(d: dt.date) -> str:
    return f"{DIAS_SEMANA[d.weekday()]} {d.day} de {MESES[d.month - 1]} de {d.year}"


def calc_vencimiento(args):
    base = dt.date.fromisoformat(args.fecha)
    direction = 1 if args.operacion == "sumar" else -1
    prorrogado = False

    if args.unidad in ("meses", "anos"):
        mult = 12 if args.unidad == "anos" else 1
        target = add_months_civil(base, direction * args.cantidad * mult)
        eff_reg = "habil_admin" if args.regimen == "habil_admin" else "habil_judicial"
        if args.prorroga and is_inhabil(target, eff_reg, args.regional):
            while is_inhabil(target, eff_reg, args.regional):
                target += dt.timedelta(days=direction)
            prorrogado = True
    elif args.cantidad == 0:
        target = base
    elif args.regimen == "corrido":
        offset = (args.cantidad - 1) if args.inicio == "mismo_dia" else args.cantidad
        target = base + dt.timedelta(days=direction * offset)
        if args.prorroga and is_inhabil(target, "habil_judicial", args.regional):
            while is_inhabil(target, "habil_judicial", args.regional):
                target += dt.timedelta(days=direction)
            prorrogado = True
    else:
        count = 0
        cursor = base
        if args.inicio == "mismo_dia" and not is_inhabil(cursor, args.regimen, args.regional):
            count = 1
        while count < args.cantidad:
            cursor += dt.timedelta(days=direction)
            if not is_inhabil(cursor, args.regimen, args.regional):
                count += 1
        target = cursor

    min_d, max_d = (base, target) if target >= base else (target, base)
    feriados = []
    bank_holidays = []
    cur = min_d + dt.timedelta(days=1)
    while cur <= max_d:
        if cur.month == 12 and cur.day == 31:
            bank_holidays.append(cur.isoformat())
        info = holiday_info(cur, args.regional)
        if info:
            feriados.append({"fecha": cur.isoformat(), "nombre": info[0], "ley": info[1]})
        cur += dt.timedelta(days=1)

    return {
        "fecha_base": base.isoformat(),
        "vencimiento": target.isoformat(),
        "vencimiento_texto": fmt_largo(target),
        "dias_corridos_totales": (max_d - min_d).days,
        "prorrogado": prorrogado,
        "feriados_en_rango": feriados,
        "alerta_feriado_bancario_31_dic": bank_holidays,
    }


def exact_calendar_diff(start: dt.date, end: dt.date):
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day
    if days < 0:
        months -= 1
        prev_m = 12 if end.month == 1 else end.month - 1
        prev_y = end.year - 1 if end.month == 1 else end.year
        days += calendar.monthrange(prev_y, prev_m)[1]
    if months < 0:
        years -= 1
        months += 12
    return {"anos": years, "meses": months, "dias": days}


def calc_diferencia(args):
    d1 = dt.date.fromisoformat(args.inicio)
    d2 = dt.date.fromisoformat(args.fin)
    start, end = (d1, d2) if d1 <= d2 else (d2, d1)
    cur = start if args.incluir_extremos else start + dt.timedelta(days=1)

    corridos = judiciales = admin = 0
    feriados = []
    bank_holidays = []
    while cur <= end:
        corridos += 1
        wd = cur.weekday()
        if cur.month == 12 and cur.day == 31:
            bank_holidays.append(cur.isoformat())
        info = holiday_info(cur, args.regional)
        if info:
            feriados.append({"fecha": cur.isoformat(), "nombre": info[0], "ley": info[1]})
        if wd != 6 and not info:
            judiciales += 1
        if wd not in (5, 6) and not info:
            admin += 1
        cur += dt.timedelta(days=1)

    return {
        "inicio": start.isoformat(),
        "fin": end.isoformat(),
        "dias_corridos": corridos,
        "dias_habiles_judiciales_ls": judiciales,
        "dias_habiles_admin_lv": admin,
        "tiempo_calendario": exact_calendar_diff(start, end),
        "feriados_en_rango": feriados,
        "alerta_feriado_bancario_31_dic": bank_holidays,
    }


def main():
    p = argparse.ArgumentParser(description="Calculadora jurídica de plazos en Chile")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("vencimiento")
    pv.add_argument("--fecha", required=True)
    pv.add_argument("--cantidad", type=int, required=True)
    pv.add_argument("--unidad", choices=["dias", "meses", "anos"], default="dias")
    pv.add_argument("--regimen", choices=["habil_judicial", "corrido", "habil_admin"], default="habil_judicial")
    pv.add_argument("--operacion", choices=["sumar", "restar"], default="sumar")
    pv.add_argument("--inicio", choices=["siguiente", "mismo_dia"], default="siguiente")
    pv.add_argument("--regional", choices=["ninguno", "arica", "chillan"], default="ninguno")
    pv.add_argument("--prorroga", action="store_true")

    pd = sub.add_parser("diferencia")
    pd.add_argument("--inicio", required=True)
    pd.add_argument("--fin", required=True)
    pd.add_argument("--regional", choices=["ninguno", "arica", "chillan"], default="ninguno")
    pd.add_argument("--incluir-extremos", action="store_true")

    args = p.parse_args()
    res = calc_vencimiento(args) if args.cmd == "vencimiento" else calc_diferencia(args)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
