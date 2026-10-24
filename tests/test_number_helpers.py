"""Validate UI numeric helpers without opening a desktop display."""
import ast
import math
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "idle_clicker_v6_6_4.py"


def load_helpers():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8-sig"), filename=str(SOURCE))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ("format_num", "clamp01")]
    assert len(nodes) == 2, "Numeric helpers missing"
    namespace = {"math": math}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec"), namespace)
    return namespace


class NumberHelpersTests(unittest.TestCase):
    def test_non_finite_values_do_not_break_ui(self):
        helpers = load_helpers()
        for value in (float("nan"), float("inf"), -float("inf"), None, "invalid"):
            with self.subTest(value=value):
                self.assertEqual(helpers["format_num"](value), "0")
                self.assertEqual(helpers["clamp01"](value), 0.0)

    def test_regular_values_remain_unchanged(self):
        helpers = load_helpers()
        self.assertEqual(helpers["format_num"](1000), "1.00K")
        self.assertEqual(helpers["clamp01"](-1), 0.0)
        self.assertEqual(helpers["clamp01"](0.4), 0.4)
        self.assertEqual(helpers["clamp01"](3), 1.0)


if __name__ == "__main__":
    unittest.main()
