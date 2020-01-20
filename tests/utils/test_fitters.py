import unittest
import numpy as np
from simulator.utils.fitter import SecondOrderFitter as SOF

class TestSecondOrderFitter(unittest.TestCase):
    def test_data_preparation(self):
        raw_data = np.array([
            [0.0, 0.0],
            [1.0, 1.0],
            [1.0, 2.0],
            [1.0, 3.0],
            [1.0, 4.0]
        ])
        dt = 0.001
        data = np.array([
            [0.000, 0.0, 0.0],
            [0.001, 1.0, 1.0],
            [0.002, 1.0, 2.0],
            [0.003, 1.0, 3.0],
            [0.004, 1.0, 4.0]
        ])
        sof = SOF(raw_data, [0,0,0], dt)
        np.testing.assert_array_equal(data, sof.data, "SOF Data preparation failed")

    def test_valid_inputs(self):
        # Not a np.ndarray
        wrong_data = [[1.0, 0.0, 1.0],[2.0, 1.0, 1.5],[3.0, 1.0, 2.0]]
        with self.assertRaises(TypeError):
            SOF(wrong_data, [0,0,0])
        # No of type float
        wrong_data = np.array([[1, 0, 1],[2, 1, 2],[3, 1, 2]])
        with self.assertRaises(TypeError):
            SOF(wrong_data, [0,0,0])
        # Not enough columns
        wrong_data = np.array([[1.0],[2.0],[3.0]])
        with self.assertRaises(ValueError):
            SOF(wrong_data, [0,0,0])
        # dt not float
        wrong_data = np.array([[0.0, 0.0],[1.0, 0.5],[1.0, 1.0]])
        with self.assertRaises(TypeError):
            SOF(wrong_data, [0,0,0], 1)
        # dt can't be negative
        wrong_data = np.array([[0.0, 0.0],[1.0, 0.5],[1.0, 1.0]])
        with self.assertRaises(ValueError):
            SOF(wrong_data, [0,0,0], -1.0)
        # Time needs to be in ascending order
        wrong_data = np.array([[0.0, 0.0, 0.0],[1.0, 1.0, 0.5],[0.5, 1.0, 1.0]])
        with self.assertRaises(ValueError):
            SOF(wrong_data, [0,0,0], 1)