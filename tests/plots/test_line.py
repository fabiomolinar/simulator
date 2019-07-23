import unittest
from simulator.models.rc import RC
from simulator.plots.line import Line

class TestLine(unittest.TestCase):
    def setUp(self):
        self.rc = RC(0.1, 100, 0.1, 0)
        self.multiplier = 10
        self.line_Q = Line(self.rc, "Q", {"multiplier": self.multiplier})
        self.line_Vc = Line(self.rc, "Vc", {})

    def test_multiplier(self):
        for _ in range(10):
            self.rc.calculate(10)
        self.assertListEqual(self.rc.Vc, self.line_Vc.get_values())
        self.assertListEqual([x * self.multiplier for x in self.rc.Q], self.line_Q.get_values())