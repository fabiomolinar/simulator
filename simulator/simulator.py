import os
import sys
import inspect
import json
import warnings
from .models.signal_generator import SignalGenerator
from .models.electric_motor import ElectricMotor
from .models.rc import RC
from .settings import simulator_settings

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
        # add models from settings/models JSON files
        self.models.update(self.load_models(path_to_models))        

    def load_models(self, path):
        """ Loads a model for each file on path """
        if not os.path.exists(path):
            warnings.warn("Path to models don't exist.")
            return {}
        models = {}
        for f in os.listdir(path):
            if f.endswith(".json"):
                f = path + "/" + f
                with open(f, "r") as rf:
                    d = json.load(rf)
                    models.update(self.add_model(d))
        return models

    def add_model(self, spec):
        """ Adds a model to the class by using a dict as specification """
        model = {}
        spec["params"]["dt"] = self.dt
        try:
            class_ = getattr(sys.modules[__name__], spec["class"])
            model = class_(**spec["params"])
        except NameError:
            warnings.warn("Couldn't instantiate a class named {}".format(spec["class"]))
            return
        self.update_execution_list(spec)
        return {spec["name"]: model}
        
    def update_execution_list(self, spec):
        """ Update the execution list after loading a new model """
        if len(self.execution_list) == 0:
            self.execution_list.append(spec)
            return
        else:
            for idx, i in enumerate(self.execution_list):
                if spec["order"] <= i["order"]:
                    self.execution_list.insert(idx, spec)
                    return
            self.execution_list.append(spec)
            
    def stop_running(self, *args):
        self.running = False
    
    def run(self, plot = None):
        for i in range(self.cycles):
            if not self.running:
                break
            self.i = i
            # run models according to position on execution list
            for model_definition in self.execution_list:
                model_inputs = self.get_model_inputs(model_definition)
                self.models[model_definition["name"]].calculate(**model_inputs)
            # update time
            self.t.append(self.t[-1] + self.dt)
            # ploting
            if plot and simulator_settings["show_plot"]:
                cycles_to_update = simulator_settings["plot_update_frequency"]/self.dt
                if cycles_to_update > 0.0:
                    cycles_to_update = int(cycles_to_update)
                    if i % (cycles_to_update) == 0.0:
                        plot.plot()
                else:
                    # Plot frequency higher than calculation frequency
                    # Will plot at every cycle
                    # NOT RECOMMENDED!!! May slow down the plotting
                    plot.plot()
        # At the end, keep plot open
        if plot and simulator_settings["show_plot"]:
            plot.end()
        print("Finished")
   
    def get_model_inputs(self, model_definition):
        """ Retrieves the necessary inputs for a model to calculate its next value """
        inputs = model_definition["inputs"]
        inputs_values = {}
        for i in inputs:
            if not "model" in inputs[i]:
                # Variable is to be taken from simulator module
                inputs_values[i] = self.get_single_value(
                    getattr(self, inputs[i]["variable"])
                )
            else:
                # Variable to be taken from a different model
                inputs_values[i] = self.get_single_value(
                    getattr(self.models[inputs[i]["model"]], inputs[i]["variable"])
                )
        return inputs_values

    @staticmethod
    def get_single_value(value):
        """ Returns the last value of a list if a list is given """
        if type(value) == list:
            return value[-1]
        return value