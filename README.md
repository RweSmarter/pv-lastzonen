# pv-lastzonen

Schnee- und Windlast-Zonen fuer PV-Carports — Cleanroom-PoC in Python (nur stdlib).

**Was es ist:** Richtwert-Rechner fuer die Vorentscheidung im Vertriebs-/Planungskontext:
- Schneelast sk nach DIN EN 1991-1-3/NA (Zonen 1/1a/2/2a/3, Hoehenformeln + Mindestwerte + Hoehengrenzen-Warnung)
- Windgrundwerte vb,0 / qb nach DIN EN 1991-1-4/NA (Zonen 1/2/2*/3/4)
- Formbeiwert mu1 fuer Pultdach-Carports (vereinfacht, Tab. 5.2)
- Grobe Zonen-Vorzuordnung je Bundesland (Interim bis Geocoding)
- Lokale Web-UI + JSON-API

**Was es NICHT ist:** Keine verbindliche Bemessung. Alle Werte sind Richtwerte mit TODO-VERIF-Markern — vor produktiver Nutzung gegen den Normtext pruefen und von einer Fachstatikerin/einem Fachstatiker absegnen lassen.

## Quickstart

```bash
python3 src/api.py 8765
# Browser: http://127.0.0.1:8765/
```

CLI:

```bash
python3 src/zonen.py 1 1 180        # Schneelastzone, Windzone, Hoehe ueber NN
```

Tests:

```bash
python3 tests/test_zonen.py
python3 tests/test_formbeiwerte.py
python3 tests/test_geobasis.py
```

## API (localhost-only)

- `GET /api/zonen?bundesland=Hessen` → Zonen-Vorschlag (Vollname oder Kuerzel)
- `GET /api/berechnen?schneezone=1&windzone=1&hoehe=180&neigung=15` → sk, qb, mu1, Dachlast, Heftigkeit

## Cleanroom-Herkunft

Implementiert aus oeffentlichen Norm-Formeln (Quellen: docs/quellen.md) — kein fremder Code, keine fremden UI-Texte. Methodik: Spec → Generierung → automatisiertes Review → Tests → Re-Pass (dokumentiert in docs/spec-cleanroom.md).

## Lizenz

MIT — siehe LICENSE.