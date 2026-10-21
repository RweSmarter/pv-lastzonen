#!/usr/bin/env python3
"""Tests fuer zonen.py — Abnahmetests aus docs/spec-cleanroom.md (Test-First)."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import zonen

def nahe(a, b, tol=0.01):
    return math.isclose(a, b, rel_tol=0, abs_tol=tol)

def test_zone1_0m_min():
    assert zonen.schneelast("1", 0) == 0.65          # Formel 0,221 -> Mindestwert

def test_zone1_400m_grenzfall():
    assert nahe(zonen.schneelast("1", 400), 0.65)    # Formel 0,650

def test_zone1_760m_formel():
    assert nahe(zonen.schneelast("1", 760), 1.467)

def test_zone3_0m_min():
    assert zonen.schneelast("3", 0) == 1.25          # Formel 0,341 -> Mindestwert

def test_zone2_600m_formel():
    assert nahe(zonen.schneelast("2", 600), 1.113)

def test_zone1a_faktor():
    # 1,25 x (0,19 + 0,91 x (140/760)^2) = 1,25 x 0,2209 = 0,276 -> min 0,81
    assert zonen.schneelast("1a", 0) == 0.81

def test_wind():
    assert zonen.windgrundwert("1") == (22.5, 0.80)
    assert zonen.windgrundwert("4") == (30.0, 1.40)
    assert zonen.windgrundwert("2*") == (25.0, 1.00)

def test_unbekannte_zone():
    try:
        zonen.schneelast("9", 0)
        assert False, "sollte ValueError werfen"
    except ValueError:
        pass
    try:
        zonen.windgrundwert("9")
        assert False, "sollte ValueError werfen"
    except ValueError:
        pass

def test_marburg():
    r = zonen.lastheftigkeit("1", "1", 180)
    assert r["sk_knm2"] == 0.65 and r["qb_knm2"] == 0.80 and r["heftigkeit"] == "moderat"

def test_hoehengrenze_helper():
    assert zonen.hoehengrenze("1") == 400
    assert zonen.hoehengrenze("3") == 800

def test_warnung_ueber_grenze():
    r = zonen.lastheftigkeit("1", "1", 500)   # 500 m > Grenze 400 m Zone 1
    assert "warnung" in r and "Hoehengrenze" in r["warnung"]

def test_keine_warnung_unter_grenze():
    r = zonen.lastheftigkeit("1", "1", 180)
    assert "warnung" not in r

def test_heftigkeit_hoch():
    r = zonen.lastheftigkeit("3", "4", 900)
    assert r["heftigkeit"] == "hoch"

if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fails = 0
    for fn in fns:
        try:
            fn(); print(f"PASS {fn.__name__}")
        except Exception as e:
            fails += 1; print(f"FAIL {fn.__name__}: {e}")
    print(f"{len(fns) - fails}/{len(fns)} PASS")
    sys.exit(1 if fails else 0)