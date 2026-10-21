# test_formbeiwerte.py -- Tests zu src/formbeiwerte.py
# Ausfuehrung: python3 tests/test_formbeiwerte.py (Repo-Root)
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

import unittest

from formbeiwerte import formbeiwert_schnee, schneelast_dach


class FormbeiwertSchneeTest(unittest.TestCase):
    def test_flach_und_knick_min(self):
        self.assertAlmostEqual(formbeiwert_schnee(0.0), 0.8)
        self.assertAlmostEqual(formbeiwert_schnee(30.0), 0.8)

    def test_linearer_bereich(self):
        self.assertAlmostEqual(formbeiwert_schnee(45.0), 0.4)

    def test_knick_max_und_steil(self):
        self.assertAlmostEqual(formbeiwert_schnee(60.0), 0.0)
        self.assertAlmostEqual(formbeiwert_schnee(75.0), 0.0)

    def test_schneelast_dach(self):
        self.assertAlmostEqual(schneelast_dach(0.65, 0.0), 0.52)
        self.assertAlmostEqual(schneelast_dach(0.65, 45.0), 0.26)

    def test_negative_neigung_valueerror(self):
        self.assertRaises(ValueError, formbeiwert_schnee, -5.0)
        self.assertRaises(ValueError, schneelast_dach, 0.65, -1.0)


if __name__ == "__main__":
    unittest.main()
