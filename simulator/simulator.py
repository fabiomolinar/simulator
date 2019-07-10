import os
import sys
import inspect
import json
import warnings
from .models.signal_generator import SignalGenerator
from .models.electric_motor import ElectricMotor
from .models.rc import RC

class Simulator:
    def __init__(self, path_to_models, dt, duration):
        self.models = {}
        self.execution_list = []
        self.t = [0]
        self.dt = dt
        self.duration = duration
        self.cycles = int(duration/dt)
        self.i = 0  # current cycle
        self.running = True
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
        self.update_execution_list(spec)

    def update_execution_list(self, spec):
        if len(self.execution_list) == 0:
            self.execution_list.append(spec)
            return
        else:
            for idx, i in enumerate(self.execution_list):
                if spec["order"] <= i["order"]:
                    self.execution_list.insert(idx, spec)
                    return
            self.execution_list.append(spec)
            
    def stop_running(self):
        self.running = False
    
    def run(self):
        for i in range(self.cycles):
            if not self.running:
                break
            self.i = i
            # run models
            for model_definition in self.execution_list:
                model_inputs = self.get_model_inputs(model_definition)
                self.models[model_definition["name"]].calculate(**model_inputs)
            # update time
            self.t.append(self.t[-1] + self.dt)

    @staticmethod
    def get_single_value(value):
        if type(value) == list:
            return value[-1]
        return value
    
    def get_model_inputs(self, model_definition):
        inputs = model_definition["inputs"]
        inputs_values = {}
        for i in inputs:
            if not "model" in inputs[i]:
                # variable is to be taken from simulator module
                inputs_values[i] = self.get_single_value(getattr(self, inputs[i]["variable"]))
            else:
                inputs_values[i] = self.get_single_value(getattr(self.models[inputs[i]["model"]], inputs[i]["variable"]))
        return inputs_values