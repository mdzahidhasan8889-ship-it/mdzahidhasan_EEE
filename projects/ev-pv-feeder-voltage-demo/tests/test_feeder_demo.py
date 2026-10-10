"""Tests for the educational EV/PV voltage approximation."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from feeder_demo import (Feeder, conservative_import_limit_kw,
                         estimate_voltage_v, import_limit_kw, synthetic_rows)

class TestFeederDemo(unittest.TestCase):
    def setUp(self):
        self.feeder = Feeder()
    def test_zero_net_power_gives_nominal_voltage(self):
        self.assertAlmostEqual(estimate_voltage_v(1, 2, 3, self.feeder), 230)
    def test_more_ev_import_lowers_voltage(self):
        self.assertLess(estimate_voltage_v(2, 3, 0, self.feeder),
                        estimate_voltage_v(1, 3, 0, self.feeder))
    def test_more_pv_increases_allowed_ev(self):
        self.assertGreater(import_limit_kw(2, 3, self.feeder),
                           import_limit_kw(0, 3, self.feeder))
    def test_conservative_limit_not_above_forecast_limit(self):
        self.assertLessEqual(conservative_import_limit_kw(4, 2, 3, self.feeder),
                             import_limit_kw(4, 3, self.feeder))
    def test_conservative_limit_maintains_lower_voltage_bound(self):
        limit = conservative_import_limit_kw(4, 2, 3, self.feeder)
        self.assertGreaterEqual(estimate_voltage_v(limit, 3, 2, self.feeder) + 1e-9,
                                self.feeder.min_voltage_v)
    def test_cap_at_charger_rating(self):
        self.assertEqual(import_limit_kw(100, 0, self.feeder), 7)
    def test_no_negative_import_limit(self):
        self.assertEqual(import_limit_kw(0, 50, self.feeder), 0)
    def test_invalid_resistance_rejected(self):
        with self.assertRaises(ValueError):
            Feeder(resistance_ohm=0)
    def test_24_synthetic_rows(self):
        rows = list(synthetic_rows(self.feeder))
        self.assertEqual(len(rows), 24)
        self.assertTrue(all(0 <= r["conservative_ev_limit_kw"] <= 7 for r in rows))
if __name__ == "__main__":
    unittest.main()
