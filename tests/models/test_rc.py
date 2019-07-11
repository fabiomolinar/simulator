import unittest
from ...models.rc import RC

class TestRC(unittest.TestCase):
    def setUp(self):
        self.dt = 0.001
        self.R = 1.
        self.C = 1.
        self.Q = 0.
        self.rc = RC(self.dt, self.R, self.C, self.Q)

    def test_initial_conditions(self):
        self.assertEqual(self.rc.Q[0], self.Q)
        self.assertEqual(self.rc.Q1[0], self.Q)

    def test_calculate(self):
        Vin = 10.0
        Vc = self.Q/self.C
        Vr = Vin - Vc
        i = Vr/self.R
        # new charge
        newQ = self.dt*((1/self.R)*(Vin-(1/self.C)*self.Q))+self.Q
        # aseserts
        self.assertAlmostEqual(self.rc.calculate(Vin), newQ)
        self.assertAlmostEqual(self.rc.Vc[-1], Vc)
        self.assertAlmostEqual(self.rc.Vr[-1], Vr)
        self.assertAlmostEqual(self.rc.i[-1], i)
