import unittest
from simulator.models.signal_generator import SignalGenerator

class TestSignalGenerator(unittest.TestCase):
    def setUp(self):
        self.init_value = 10
        self.step_value = 5
        self.events = [
            {
                "start": {
                    "value": self.init_value
                }
            },
            {
                "step": {
                    "cycle": 1,
                    "value": self.step_value
                }
            },
            {
                "ramp_up": {
                    "cycle": 2,
                    "value": 1   # increase in output per cycle
                }
            },
            {
                "ramp_down": {
                    "cycle": 4,
                    "value": 1   # increase in output per cycle
                }
            },
            {
                "pause": {
                    "cycle": 6
                }
            }
        ]
        self.sig = SignalGenerator(self.events)

    def test_initial_conditions(self):
        self.assertEqual(self.sig.current_value[0], self.init_value)

    def test_calculate(self):
        # On first cycle we keep the initial value
        self.sig.calculate(0)
        self.assertEqual(self.sig.current_value[-1], self.init_value)
        # Check step
        self.sig.calculate(1)
        self.assertEqual(self.sig.current_value[-1], self.step_value)
        # Check ramp up
        self.sig.calculate(2)
        self.sig.calculate(3)
        self.assertEqual(self.sig.current_value[-1], self.step_value + 2)
        # Check rampdown
        self.sig.calculate(4)
        self.sig.calculate(5)
        self.assertEqual(self.sig.current_value[-1], self.step_value + 2 - 2)
        # Check pause
        self.sig.calculate(6)
        self.sig.calculate(7)
        self.assertEqual(self.sig.current_value[-1], self.step_value + 2 - 2)

