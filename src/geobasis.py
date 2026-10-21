# -*- coding: utf-8 -*-
"""Geobasis-Vorzuordnung Schneelast-/Windzone je Bundesland (PoC-Interim).

Liefert nur den ueblichen Dominanzwert je Bundesland; keine Geocoding-
Ersatzfunktion. Verbindliche Zonenzuordnung erst ab Stufe 2+.
"""

# --- Daten --------------------------------------------------------------

# Quelle: docs/quellen.md [Q-KARTEN-SCHNEE] — uebliche Zonenzuordnung der
# Laender laut Schneelastzonenkarten (Standard-Literatur, Kartenwerk).
# ALLES TODO-VERIF: nur Dominanzwert, Mittelgebirgs-/Alpenlagen hoeher.
SCHNEE_BL = {
    "SH": "1", "MV": "1", "HH": "1", "HB": "1",
    "NI": "1", "BE": "1", "BB": "1", "RP": "1",
    "ST": "2", "NW": "2", "HE": "2",
    "SL": "2", "BW": "2", "BY": "2", "TH": "2", "SN": "2",
}  # TODO-VERIF (Kartenwerk, Stufe 2+ ersetzt durch Geocoding)

# Alias: Vollname -> Kuerzel (API/UI-Ergonomie; ISO 3166-2:DE ohne Praefix DE-)
ALIAS = {
    "Schleswig-Holstein": "SH", "Mecklenburg-Vorpommern": "MV", "Hamburg": "HH",
    "Bremen": "HB", "Niedersachsen": "NI", "Berlin": "BE", "Brandenburg": "BB",
    "Rheinland-Pfalz": "RP", "Sachsen-Anhalt": "ST", "Nordrhein-Westfalen": "NW",
    "Hessen": "HE", "Saarland": "SL", "Baden-Württemberg": "BW", "Bayern": "BY",
    "Thüringen": "TH", "Sachsen": "SN",
}

# Quelle: docs/quellen.md [Q-KARTEN-WIND] — uebliche Zonenzuordnung der
# Laender laut Windzonenkarten (Standard-Literatur, Kartenwerk).
# TODO-VERIF: BY teils Zone 2; Kuestenlage (SH/MV/HH/HB) lokal hoeher.
WIND_BL = {
    "SH": "2", "MV": "2", "HH": "2", "HB": "2",
    "NI": "2", "BY": "2",
    "BE": "1", "BB": "1", "ST": "1", "SN": "1", "TH": "1",
    "NW": "1", "HE": "1", "RP": "1", "SL": "1", "BW": "1",
}  # TODO-VERIF (Kartenwerk, Stufe 2+ ersetzt durch Geocoding)

# --- Funktionen ---------------------------------------------------------

_HINWEIS = (
    "Dominanzwert je Bundesland; Mittelgebirgs-/Alpen- und Kuestenlagen "
    "liegen abweichend hoeher. Nicht verbindlich; amtliche Karte oder "
    "Geocoding-Standort ist massgebend."
)


def zonen_vorschlag(bundesland: str) -> dict:
    """Grobe Zonen-Vorzuordnung fuer ein Bundesland.

    Args:
        bundesland: Laenderkuerzel nach ISO 3166-2:DE (z. B. "HE").

    Returns:
        dict mit schnee, wind, verbindlich=False, hinweis.

    Raises:
        ValueError: bei unbekanntem Laenderkuerzel.
    """
    # Referenz: [Q-NORM-ISO-3166-2] ISO 3166-2:DE Laenderkuerzel (TODO-VERIF).
    # Vollname exakt (UI-Konvention), Kuerzel tolerant gegen Whitespace/Gross-/Kleinschreibung.
    roh = str(bundesland).strip()
    schluessel = ALIAS.get(roh, roh.upper())
    if schluessel not in SCHNEE_BL or schluessel not in WIND_BL:
        raise ValueError("unbekanntes Bundesland: %r" % (bundesland,))
    return {
        "schnee": SCHNEE_BL[schluessel],
        "wind": WIND_BL[schluessel],
        "verbindlich": False,
        "hinweis": _HINWEIS,
    }


def laender() -> list:
    """Sortierte Liste aller erfassten Bundeslaender (Kuerzel)."""
    return sorted(set(SCHNEE_BL) & set(WIND_BL))
