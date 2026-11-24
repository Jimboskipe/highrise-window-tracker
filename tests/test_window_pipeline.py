"""Unit tests for High-Rise Window Warehouse-to-GC-Turnover Pipeline.

Run:  python -m unittest discover -s tests -v
"""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import window_pipeline as wp  # noqa: E402


class WindowPipelineTests(unittest.TestCase):
    def test_every_floor_window_count_reconciles(self):
        for f in wp.sample_15_story_tower():
            self.assertEqual(f.total_windows, f.accounted_total, f"Floor {f.floor} mismatch")

    def test_warehouse_has_two_adjacent_rooms_and_9ft_row_pitch(self):
        wh = wp.WAREHOUSE_SPEC
        self.assertEqual(wh["total_sq_ft"], 2000)
        self.assertEqual(wh["row_spacing_ft"], 9)
        self.assertEqual(wh["max_pallets_per_row"], 8)
        self.assertEqual(len(wh["rooms"]), 2)
        for rm in wh["rooms"]:
            for r in rm["rows"]:
                self.assertLessEqual(r["pallets_loaded"], 8)

    def test_three_checklist_areas_present(self):
        self.assertEqual(len(wp.CHECKLIST_AREAS), 3)

    def test_export_json_unaccounted_is_zero(self):
        tmp = os.path.join(tempfile.mkdtemp(), "window_data.json")
        d = wp.export_window_json(tmp)
        self.assertEqual(d["totals"]["unaccounted"], 0)
        self.assertEqual(len(d["floors"]), 15)


if __name__ == "__main__":
    unittest.main()
