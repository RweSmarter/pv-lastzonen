# Quellen (R-246 Provenance-Gate)

## Verifiziert 21.10.2026 (Web-Recherche, 4+ Quellen konsistent)
- Schneelast-Formeln Zone 1/1a/2/3: Nds. MBl. Nr. 37/2012 (niedersachsen.de/download/80801, Anlagenband 37b, DIN EN 1991-1-3/NA Fassung Sep 2012) + hausbauexperte.net + friedrich-datentechnik.de (Basiswissen-Schneelast.pdf) — Formeln identisch:
  - Zone 1: sk = 0,19 + 0,91·((A+140)/760)²
  - Zone 1a: 1,25 × Zone-1-Formel
  - Zone 2: sk = 0,25 + 0,91·((A+140)/760)²
  - Zone 3: sk = 0,31 + 0,91·((A+140)/760)²
- Mindestwert Zone 1: 0,65 kN/m² bis 400 m NN (lamilux.de + hausbauexperte.net)
- Windzonen-Struktur 1/2/2*/3/4 + Norm DIN EN 1991-1-4/NA:2010-12 (dlubal.com Lastzonen-Tool, Last Update 09/2026)

## TODO-VERIF (PoC-Richtwerte, Pruefung durch Fachstatiker vor produktiver Nutzung)
- Mindestwerte Zone 1a (0,81), Zone 2 (0,85), Zone 2a (1,10), Zone 3 (1,25) + Hoehengrenzen (400/400/600/600/800 m): Standard-Literatur, gegen Normtext Tabelle A.1 zu verifizieren
- Windgrundwerte qb: Zone 1 = 0,80, Zone 2 = 1,00, Zone 2* = 1,00, Zone 3 = 1,20, Zone 4 = 1,40 kN/m² (vb,0 = 22,5/25,0/25,0/27,5/30,0 m/s): Standard-Literatur, gegen NA zu verifizieren
- Zone 2a-Formel (1,50 × Zone-1-Formel): Standard-Literatur, zu verifizieren