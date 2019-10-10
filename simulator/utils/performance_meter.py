import warnings
import sys
from .numerical_analysis import DumbDifferentiator
from ..settings import simulator_settings

class PerformanceMeter:
    def __init__(self, sim, config = None):
        self.sim = sim
        self.config = config if config else simulator_settings["performance_meter"]
        self.enabled = self.is_enabled(config)
        self.measurements = self.get_measurements(config)

    def is_enabled(self, config):
        if config["enabled"]:
            return True
        else:
            return False

    def get_measurements(self, config):
        measurements = {}
        for mea in config["measurements"]:
            try:
                class_ = getattr(sys.modules[__name__], mea["class"])
                instance_ = class_(mea["settings"])
                measurements[mea["name"]] = instance_
            except NameError:
                warnings.warn("Couldn't instantiate a class named {}".format(mea["class"]))
                continue
        return measurements
    
    def calculate(self):
        for mea in self.measurements:
            self.measurements[mea].calculate(self.sim)

    def result_to_string(self):
        result = ""
        for mea in self.measurements:
            result += self.measurements[mea].result_to_string()
        if result == "":
            return "No measurements to show. "
        return result

class ModelProxy:
    def get_value(self, settings, sim):
        instance_ = sim.models[settings["object_name"]]
        return getattr(instance_, settings["attribute"])

    def result_to_string(self):
        return "Result string not defined for {}. ".format(self.__class__.__name__)

class Overshoot(ModelProxy):
    def __init__(self, settings):
        self.Y_settings = settings["Y"]
        self.SP_settings = settings["SP"]
        self.base = None
        self.max = 0

    def calculate(self, sim):
        Y = self.get_value(self.Y_settings, sim)[-1]
        SP = self.get_value(self.SP_settings, sim)[-1]
        if not self.base:
            self.base = Y - SP
        overshoot = (SP - Y)/self.base
        if overshoot > self.max:
            self.max = overshoot
        return self.max

    def result_to_string(self):
        return "Max overshoot = {}. ".format(self.max)

class SettlingTime(ModelProxy):
    def __init__(self, settings):
        self.Y_settings = settings["Y"]
        self.SP_settings = settings["SP"]
        self.dx_threshold = settings["dx_threshold"]
        self.dx_cycles_hold = settings["dx_cycles_hold"]
        self.range = settings["range"]
        self.D = DumbDifferentiator()
        self.cycles_held = 0
        self.settled = False
        self.settle_time = 0

    def calculate(self, sim):
        Y = self.get_value(self.Y_settings, sim)[-1]
        SP = self.get_value(self.SP_settings, sim)[-1]
        if not self.settled and self.within_range(Y, SP) and self.stabilized(Y, sim):
            self.settled = True
            self.settle_time = sim.t[-1]
            return self.settle_time

    def within_range(self, Y, SP):
        absolute_difference = abs((Y-SP)/SP)
        return absolute_difference < self.range

    def stabilized(self, Y, sim):
        derivative = self.D.calculate(sim.dt, Y)
        if derivative < self.dx_threshold:
            self.cycles_held += 1
        else:
            self.cycles_held = 0
        return self.cycles_held > self.dx_cycles_hold

    def result_to_string(self):
        if not self.settled:
            return "System didn't stabilize. "
        else:
            return "Settle time = {}. ".format(self.settle_time)