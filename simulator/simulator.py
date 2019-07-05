import os
import sys
import inspect
import json
import warnings
from .models.signal_generator import SignalGenerator
from .models.electric_motor import ElectricMotor
from .models.rc import RC

class Simulator:
    def __init__(self, path_to_models, dt):
        self.models = {}
        self.dt = dt
        self.path_to_models = path_to_models
        
        self.load_models(path_to_models)

    def load_models(self, path):
        """ Loads a model for each file on path """
        if not os.path.exists(path):
            warnings.warn("Path to models don't exist.")
        for f in os.listdir(path):
            if f.endswith(".json"):
                f = path + "/" + f
                with open(f, "r") as rf:
                    d = json.load(rf)
                    self.add_model(d)

    def add_model(self, spec):
        """ Adds a model to the class by using a dict as specification """
        spec["params"]["dt"] = self.dt
        try:
            class_ = getattr(sys.modules[__name__], spec["class"])
            model = class_(**spec["params"])
        except NameError:
            warnings.warn("Couldn't instantiate a class named {}".format(spec["class"]))
            return
        self.models[spec["name"]] = model
        