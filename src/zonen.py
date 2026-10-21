#!/usr/bin/env python3
"""zonen.py — Schneelast-/Windzonen (Cleanroom-PoC, 21.10.2026)

Cleanroom-Regel: implementiert aus oeffentlichen Norm-Formeln (DIN EN 1991-1-3/NA,
DIN EN 1991-1-4/NA), NICHT aus fremdem Code. Quellen: docs/quellen.md.
Richtwerte fuer Vorentscheidung — verbindliche Bemessung = Fachstatiker.
Nur stdlib. """
# (Formel-Typ, Faktor, Offset, Mindestwert kN/m2, Hoehengrenze m) — docs/quellen.md
SCHNEE = {
    "1":   ("basis", 1.00, 0.19, 0.65, 400),
    "1a":  ("basis", 1.25, 0.19, 0.81, 400),
    "2":   ("basis", 1.00, 0.25, 0.85, 600),
    "2a":  ("basis", 1.50, 0.19, 1.10, 600),  # TODO-VERIF: Faktor 1,50
    "3":   ("basis", 1.00, 0.31, 1.25, 800),
}
# (vb,0 m/s, qb kN/m2) — TODO-VERIF gegen NA
WIND = {"1": (22.5, 0.80), "2": (25.0, 1.00), "2*": (25.0, 1.00),
        "3": (27.5, 1.20), "4": (30.0, 1.40)}

def schneelast(zone, hoehe_nn):
    """Charakteristische Schneelast sk (kN/m2) nach Zone + Hoehe ueber NN.

    Oberhalb der Hoehengrenze der Zone (siehe hoehengrenze()) ist die
    Zonenzuordnung selbst gegen die Norm zu pruefen — sk hier ist ein Richtwert.
    """
    z = SCHNEE.get(str(zone))
    if z is None:
        raise ValueError(f"unbekannte Schneelastzone {zone!r} (erlaubt: {sorted(SCHNEE)})")
    _, faktor, offset, minimum, grenze = z
    a = max(0.0, float(hoehe_nn))
    sk = faktor * (offset + 0.91 * ((a + 140.0) / 760.0) ** 2)
    return round(max(sk, minimum), 3)

def hoehengrenze(zone):
    """Hoehengrenze (m ueber NN) der Schneelastzone (docs/quellen.md, TODO-VERIF)."""
    z = SCHNEE.get(str(zone))
    if z is None:
        raise ValueError(f"unbekannte Schneelastzone {zone!r} (erlaubt: {sorted(SCHNEE)})")
    return z[4]

def windgrundwert(zone):
    """(vb0 in m/s, qb in kN/m2) nach Windzone. Zonenschluessel: 1, 2, 2*, 3, 4."""
    z = WIND.get(str(zone))
    if z is None:
        raise ValueError(f"unbekannte Windzone {zone!r} (erlaubt: {sorted(WIND)})")
    return z

def lastheftigkeit(schnee_zone, wind_zone, hoehe_nn):
    """Kombi-Verdict fuer Angebot/Report (Richtwert-Text)."""
    sk = schneelast(schnee_zone, hoehe_nn)
    vb0, qb = windgrundwert(wind_zone)
    # Schwellen bewusst: hoch ab sk 1,10 (Zone 2a/3) oder qb 1,20 (Zone 3/4)
    heftig = "hoch" if sk >= 1.10 or qb >= 1.20 else ("mittel" if sk >= 0.85 or qb >= 1.00 else "moderat")
    out = {"sk_knm2": sk, "vb0_ms": vb0, "qb_knm2": qb, "heftigkeit": heftig,
           "hinweis": "Richtwerte (Cleanroom-PoC) — verbindliche Bemessung durch Fachstatiker."}
    grenze = hoehengrenze(schnee_zone)
    if max(0.0, float(hoehe_nn)) > grenze:
        out["warnung"] = (f"Hoehe {float(hoehe_nn):.0f} m liegt ueber der Hoehengrenze "
                          f"{grenze} m der Schneelastzone {schnee_zone} — Zonenzuordnung "
                          "und Wert gegen Norm pruefen.")
    return out

if __name__ == "__main__":
    import json, sys
    try:
        z_s, z_w = sys.argv[1], sys.argv[2]
        h = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    except (IndexError, ValueError):
        print("Usage: zonen.py <schneezone> <windzone> [hoehe_nn_m]", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(lastheftigkeit(z_s, z_w, h), ensure_ascii=False, indent=2))