# formbeiwerte.py -- Formbeiwerte fuer Schneelast auf Pultdach-Carports
# Umfang: DIN EN 1991-1-3, Tabelle 5.2 (vereinfachter PoC-Ausschnitt), nur stdlib.

__all__ = [
    "MU1_MAX",
    "NEIGUNG_MIN",
    "NEIGUNG_MAX",
    "formbeiwert_schnee",
    "schneelast_dach",
    "hinweis_stau",
]

# Quelle: docs/quellen.md, Eintrag "DIN EN 1991-1-3" (Tab. 5.2, Pultdach, Grundwert mu1)
MU1_MAX = 0.8  # TODO-VERIF gegen Tab. 5.2

# Quelle: docs/quellen.md, Eintrag "DIN EN 1991-1-3" (Tab. 5.2, Knickpunkte der Falllinie)
NEIGUNG_MIN = 30.0  # TODO-VERIF gegen Tab. 5.2
NEIGUNG_MAX = 60.0  # TODO-VERIF gegen Tab. 5.2


def formbeiwert_schnee(neigung_grad: float) -> float:
    """Formbeiwert mu1 fuer Schneelast auf Pultdach.

    0-30 Grad konstant MU1_MAX, 30-60 Grad linear MU1_MAX -> 0.0,
    ab 60 Grad 0.0. PoC-Vereinfachung: stetige Falllinie statt
    abgestufter Tabellenfuehrung, ohne Zwischenstufen/Sonderfaelle.

    ValueError bei negativer Neigung.
    """
    if neigung_grad < 0.0:
        raise ValueError(f"Neigung darf nicht negativ sein: {neigung_grad} Grad")
    if neigung_grad <= NEIGUNG_MIN:
        return MU1_MAX
    if neigung_grad >= NEIGUNG_MAX:
        return 0.0
    anteil = (neigung_grad - NEIGUNG_MIN) / (NEIGUNG_MAX - NEIGUNG_MIN)
    return MU1_MAX * (1.0 - anteil)


def schneelast_dach(sk: float, neigung_grad: float) -> float:
    """Schneelast auf Dachflaeche: sk * mu1.

    Sonderlastfall Schneebelastung des PoC. Bewusst ohne Zuschlaege
    fuer Schneebagging (Auflast ueber/nach PV-Modulen) sowie ohne
    Abrutschen/Stau; siehe hinweis_stau().
    """
    return sk * formbeiwert_schnee(neigung_grad)


def hinweis_stau() -> str:
    """Fester Hinweistext zu Stauszenarien im PoC-Umfang (Stufe 1)."""
    return ("Stauszenarien (z. B. Schneefang, Nachbarbauwerk) sind im PoC "
            "nicht abgebildet und werden in Stufe 2 behandelt.")
