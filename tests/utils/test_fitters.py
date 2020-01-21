import unittest
import numpy as np
from simulator.utils.fitter import SecondOrderFitter as SOF

class TestSecondOrderFitter(unittest.TestCase):
    def test_fitter(self):
        # Expected results
        k, e, w = 2.0, 0.5, 1.0
        # Create test data using class' integrator
        raw_data = np.ones([10,2])
        raw_data[0] = [0,0]
        sof = SOF(raw_data, [k, e, w], 1.0)
        y = sof.integrate([k, e, w])
        raw_data = sof.data
        raw_data[:,2] = y.T
        # Do test
        initial_guess = [k+1, e+2, w+1]
        sof_to_test = SOF(raw_data, initial_guess)
        sof_to_test.fit()
        results = [sof_to_test.k, sof_to_test.e, sof_to_test.w]
        np.testing.assert_array_almost_equal([k, e, w], results, 3, "SOF fitter didn't find the correct result")

    def test_integration(self):
        # Create array with a step input
        raw_data = np.ones([10,2])
        raw_data[0] = [0,0]
        sof = SOF(raw_data, [2,0.5,1], 1.0)
        y = sof.integrate([2,0.5,1])
        result = np.array(
            [0.0, 0.6805863077289664, 1.6985568968787739, 2.248515488778333, 
            2.306321146828116, 2.149384237407534, 2.004736348427006, 
            1.9487540245272295, 1.9579675589078076, 1.9858099387006853]
        )
        np.testing.assert_array_almost_equal(y, result, 6, "ODE integration not working properly")

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