# Cleanroom-Spec: PV-Carport-Statik-Modul „zonen" (PoC, 21.10.2026)

## Zweck
Beweis des Cleanroom-Musters (ArtCraft-Konzept, P3): marktgängige Funktionalität (Lastzonenermittlung, wie in Statik-Software) als eigenes Open-Source-Modul nachprogrammieren — aus oeffentlichen Norm-Formeln, NICHT aus fremdem Code.

## Cleanroom-Regeln (Playbook-Kern)
1. Quelle = Norm-Formeln + oeffentliche Tabellen (DIN EN 1991-1-3/NA, DIN EN 1991-1-4/NA). Kein Dekompilat, kein fremder Quellcode, keine UI-Texte.
2. Jede Konstante mit Quellenangabe in docs/quellen.md. Unverifizierte Werte als TODO-VERIF markiert.
3. Eigene Namen, eigene Struktur, eigene Tests.
4. Grenze: Richtwerte fuer Vorentscheidung. Verbindliche Bemessung = Fachstatiker (hier: Commander).

## Feature-Matrix (PoC-Scope)
| Feature | Status |
|---|---|
| Schneelast sk nach Zone + Hoehe NN (Zonen 1, 1a, 2, 2a, 3, Formeln + Mindestwerte) | PoC |
| Windgrundwert vb,0 / qb nach Zone (1, 2, 2*, 3, 4) | PoC |
| Lastheftigkeit-Verdict (Kombi-Text fuer Angebot/Report) | PoC |
| Zonenzuordnung aus Adresse/Karte | Stufe 2 (Geocoding) |
| Formbeiwerte Dach, Stau, Schneefang | Stufe 2+ |
| GUI | Stufe 3 |

## Abnahmetests (Test-First)
- Zone 1 @ 0 m: sk = min 0,65 kN/m² (Formel ergibt 0,221)
- Zone 1 @ 400 m: sk ≈ 0,65 (Formel 0,650 — Grenzfall)
- Zone 1 @ 760 m: sk ≈ 1,467 (Formel > Mindestwert)
- Zone 3 @ 0 m: sk = min 1,25 (Formel 0,341)
- Zone 2 @ 600 m: sk ≈ 1,113 (Formel > Mindestwert 0,85)
- Wind Zone 1: qb = 0,80 kN/m² | Zone 4: qb = 1,40
- Unbekannte Zone -> ValueError
- Marburg-Beispiel (Zone 1, 180 m): sk = 0,65 (min), qb = 0,80

## Nicht-Ziele
- Kein Prod-Deploy; verbindliche Bemessung bleibt Fachstatik.
- Keine Ersetzung der Fachstatik — Entscheidungsunterstuetzung im Vertriebskontext.