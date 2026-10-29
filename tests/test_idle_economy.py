"""No display, user save, or external dependencies needed."""
import math
import unittest

from idle_economy import (
    cost_of_next, describe_advice, format_duration, recommend_purchase,
)


UPGRADES = [
    ("A", 15, 1.15, 0.1),
    ("B", 150, 1.15, 1.0),
    ("C", 1200, 1.15, 8.0),
]


class PurchaseAdvisorTests(unittest.TestCase):
    def test_growth_tracks_owned_count(self):
        self.assertEqual(cost_of_next(15, 1.15, 0), 15)
        self.assertEqual(cost_of_next(15, 1.15, 1), 17)
        self.assertEqual(cost_of_next(15, 1.15, 2), 20)

    def test_roi_consistent_on_tie_uses_lower_cost(self):
        advice = recommend_purchase(UPGRADES, {}, gold=0, cps=5)
        self.assertEqual(advice.name, "A")
        self.assertEqual(advice.seconds_until_affordable, 3)
        self.assertAlmostEqual(advice.payback_seconds, 150)

    def test_affordability_and_prestige(self):
        advice = recommend_purchase([UPGRADES[1]], {}, gold=160, cps=10,
                                    prestige_multiplier=2)
        self.assertEqual(advice.name, "B")
        self.assertEqual(advice.seconds_until_affordable, 0)
        self.assertAlmostEqual(advice.extra_cps, 2)
        self.assertAlmostEqual(advice.payback_seconds, 75)
        self.assertIn("achetable maintenant", describe_advice(advice))

    def test_zero_cps_requires_clicks_without_fake_eta(self):
        advice = recommend_purchase(UPGRADES, {}, 0, 0)
        self.assertIsNone(advice.seconds_until_affordable)
        self.assertIn("à financer par clics", describe_advice(advice))

    def test_upgrade_cost_after_owned_counts_changes_best_choice(self):
        advice = recommend_purchase(UPGRADES[:2], {"A": 8, "B": 0}, 100, 10)
        self.assertEqual(advice.name, "B")

    def test_excludes_unusable_economic_states(self):
        for invalid in (float("nan"), float("inf"), -5):
            self.assertIsNone(recommend_purchase(UPGRADES, {}, invalid, 0))
            self.assertIsNone(recommend_purchase(UPGRADES, {}, 0, invalid))
        self.assertIsNone(recommend_purchase([], {}, 0, 0))
        self.assertTrue(math.isinf(cost_of_next(15, 1.15, 1000000)))
        self.assertTrue(math.isinf(cost_of_next(15, 0.5, 0)))

    def test_format_duration(self):
        self.assertEqual(format_duration(0), "1 s")
        self.assertEqual(format_duration(60), "1 min")
        self.assertEqual(format_duration(3600), "1 h")
        self.assertEqual(format_duration(86400), "1 j")


if __name__ == "__main__":
    unittest.main()
