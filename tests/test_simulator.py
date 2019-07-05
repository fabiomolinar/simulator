import os
import unittest
from simulator import settings
from simulator.simulator import Simulator
from simulator.models import (rc, electric_motor, signal_generator)

class TestLoadModelsMethod(unittest.TestCase):
    def setUp(self):
        self.path_to_models = settings.simulator_settings["path_to_models"]
        self.S = Simulator(self.path_to_models)

    def test_load_models(self):
        self.assertEqual(1,1)

