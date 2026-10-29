"""Regression tests: Max must equal repeated real unit purchases, without GUI."""
import math
import random
import unittest

from idle_economy import cost_of_next, plan_bulk_purchase


def naive(base, growth, owned, gold):
    count = 0
    spent = 0
    while True:
        cost = round(base * (growth ** (owned + count)))
        if spent + cost > int(gold):
            break
        spent += cost
        count += 1
    return count, spent


class ExactBulkTests(unittest.TestCase):
    def test_matches_unit_by_unit_rounding_for_random_economies(self):
        rng = random.Random(20261029)
        for _ in range(250):
            base = rng.choice([15, 150, 1200, 15000, 250000])
            growth = rng.choice([1.1, 1.15, 1.25, 1.5])
            owned = rng.randrange(0, 25)
            gold = rng.randrange(0, 2_000_000) + rng.choice([0, 0.25, 0.75])
            expected_qty, expected_spent = naive(base, growth, owned, gold)
            batch = plan_bulk_purchase(base, growth, owned, gold)
            self.assertEqual((batch.quantity, batch.spent), (expected_qty, expected_spent))
            self.assertAlmostEqual(batch.remaining_gold, gold - expected_spent)
            self.assertFalse(batch.capped)

    def test_individual_rounding_differs_from_closed_form(self):
        # 15 + round(15*1.15)=17 + round(15*1.15^2)=20, total=52
        batch = plan_bulk_purchase(15, 1.15, 0, 52)
        self.assertEqual((batch.quantity, batch.spent, batch.remaining_gold), (3, 52, 0))
        self.assertEqual(plan_bulk_purchase(15, 1.15, 0, 51).quantity, 2)

    def test_cap_is_visible_and_not_a_false_max_claim(self):
        batch = plan_bulk_purchase(15, 1.15, 0, 1000000, max_units=2)
        self.assertEqual(batch.quantity, 2)
        self.assertEqual(batch.spent, 32)
        self.assertTrue(batch.capped)

    def test_very_large_gold_cannot_stall_or_purchase_free_units(self):
        batch = plan_bulk_purchase(15, 1.15, 0, 1e200)
        self.assertGreater(batch.quantity, 1000)
        self.assertLess(batch.quantity, 10000)
        self.assertFalse(batch.capped)
        self.assertGreater(batch.spent, 0)
        self.assertTrue(math.isfinite(batch.remaining_gold))
        self.assertGreater(batch.remaining_gold, 0)

    def test_unusable_inputs_never_generate_purchases(self):
        for bad in (float("nan"), float("inf"), -1):
            self.assertEqual(plan_bulk_purchase(15, 1.15, 0, bad).quantity, 0)
        self.assertEqual(plan_bulk_purchase(15, 1.15, -1, 200).quantity, 0)
        self.assertEqual(plan_bulk_purchase(0, 1.15, 0, 200).quantity, 0)
        self.assertEqual(plan_bulk_purchase(15, 0.5, 0, 200).quantity, 0)
        self.assertEqual(plan_bulk_purchase(15, 1.15, 0, 200, max_units=0).quantity, 0)
        self.assertTrue(math.isinf(cost_of_next(15, 1.15, 1000000)))


if __name__ == "__main__":
    unittest.main()
