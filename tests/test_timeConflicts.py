import unittest
from datetime import time
from app.logic.timeConflicts import slots_overlap


class SlotsOverlapTest(unittest.TestCase):

    def test_exact_same_slot(self):
        self.assertTrue(slots_overlap("MWF", time(9, 20), time(10, 30),
                                      "MWF", time(9, 20), time(10, 30)))

    def test_partial_overlap(self):
        self.assertTrue(slots_overlap("TR", time(10, 40), time(11, 50),
                                      "TR", time(10, 40), time(12, 30)))

    def test_one_inside_other(self):
        self.assertTrue(slots_overlap("M", time(9, 0), time(12, 0),
                                      "M", time(10, 0), time(11, 0)))

    def test_touching_times_do_not_conflict(self):
        self.assertFalse(slots_overlap("MWF", time(9, 20), time(10, 30),
                                       "MWF", time(10, 30), time(11, 40)))

    def test_same_time_different_days(self):
        self.assertFalse(slots_overlap("MWF", time(9, 20), time(10, 30),
                                       "TR", time(9, 20), time(10, 30)))

    def test_share_one_day(self):
        self.assertTrue(slots_overlap("MW", time(9, 0), time(10, 0),
                                      "WF", time(9, 30), time(10, 30)))

    def test_no_days(self):
        self.assertFalse(slots_overlap("", time(9, 0), time(10, 0),
                                       "M", time(9, 0), time(10, 0)))


if __name__ == "__main__":
    unittest.main()
