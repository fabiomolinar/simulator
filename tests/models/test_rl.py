import unittest
from simulator.models.rl import RL

class TestRL(unittest.TestCase):
    def setUp(self):
        self.dt = 0.001
        self.R = 1.
        self.L = 1.
        self.i = 0.
        self.rl = RL(self.dt, self.R, self.L, self.i)

    def test_initial_conditions(self):
        self.assertEqual(self.rl.i[0], self.i)
        self.assertEqual(self.rl.i1[0], self.i)

    def test_calculate(self):
        Vin = 10.0
        Vr = self.i*self.R
        Vl = Vin - Vr
        newi = self.dt*Vl/self.L + self.i
        # aseserts
        self.assertAlmostEqual(self.rl.calculate(Vin), newi)
        self.assertAlmostEqual(self.rl.Vr[-1], Vr)
        self.assertAlmostEqual(self.rl.Vl[-1], Vl)
