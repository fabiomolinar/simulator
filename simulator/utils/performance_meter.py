import warnings
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
        measurements = []
        for mea in config["measurements"]:
            try:
                class_ = getattr(sys.modules[__name__], mea["class"])
                instance_ = class_(**mea["settings"])
                measurements.append(instance_)
            except NameError:
                warnings.warn("Couldn't instantiate a class named {}".format(mea["class"]))
                continue
        return measurements
    
    def calculate(self):
        for mea in self.measurements:
            mea.calculate(self.sim)

class ModelProxy:
    def get_value(self, settings, sim):
        instance_ = sim.models[settings["object_name"]]
        return getattr(instance_, settings["attribute"])

class Overshoot(ModelProxy):
    def __init__(self, settings):
        self.Y_settings = settings["Y"]
        self.SP_settings = settings["SP"]
        self.max = 0

    def calculate(self, sim):
        Y = self.get_value(self.Y_settings, sim)
        SP = self.get_value(self.SP_settings, sim)
        overshoot = Y/SP
        if overshoot > self.max:
            self.max = overshoot
        return self.max

class SettlingTime(ModelProxy):
    def __init__(self, settings):
        self.Y_settings = settings["Y"]
        self.SP_settings = settings["SP"]
        self.dx_threshold = settings["dx_threshold"]
        self.range = settings["range"]
        self.D = DumbDifferentiator()

    def calculate(self, sim):
        Y = self.get_value(self.Y_settings, sim)
        SP = self.get_value(self.SP_settings, sim)
        if self.within_range(Y, SP) and self.stabilized(Y, sim):
            return 

    def within_range(self, Y, SP):
        absolute_difference = abs((Y-SP)/SP)
        return absolute_difference < self.range

    def stabilized(self, Y, sim):
        derivative = self.D.calculate(sim.dt, Y)
        return derivative < self.dx_threshold