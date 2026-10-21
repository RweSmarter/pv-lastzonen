# -*- coding: utf-8 -*-
"""Tests fuer geobasis.py — ausfuehrbar: python3 test_geobasis.py (sys.path -> src/)"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/src")

from geobasis import laender, zonen_vorschlag

def test_alias_vollname():
    r = zonen_vorschlag("Hessen")
    assert r["schnee"] == "2" and r["wind"] == "1"

# HE: Schneelast 2, Wind 1, nicht verbindlich
r = zonen_vorschlag("HE")
assert r["schnee"] == "2", r
assert r["wind"] == "1", r
assert r["verbindlich"] is False, r
assert isinstance(r["hinweis"], str) and r["hinweis"], r

# BY: Windzone 2 (TODO-VERIF-Regel aus Spec)
assert zonen_vorschlag("BY")["wind"] == "2"
# Normalisierung: Klein-/Mischschreibung
assert zonen_vorschlag(" he ")["schnee"] == "2"
# Unbekanntes Land -> ValueError
try:
    zonen_vorschlag("XYZ")
except ValueError:
    pass
else:
    raise AssertionError("XYZ musste ValueError ausloesen")
# laender(): 16 Eintraege, sortiert
lst = laender()
assert len(lst) == 16, lst
assert lst == sorted(lst)
# Konsistenz: schnee/wind-Werte gueltig
for k in lst:
    v = zonen_vorschlag(k)
    assert v["schnee"] in ("1", "2"), (k, v)
    assert v["wind"] in ("1", "2"), (k, v)

print("OK: alle Tests bestanden")
