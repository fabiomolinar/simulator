import os
import warnings
import json
import matplotlib.pyplot as plt
from ..settings import simulator_settings

class Plot:
    def __init__(self, path_to_models, sim):
        if not simulator_settings["show_plot"]:
            return
        self.path_to_models = path_to_models
        self.sim = sim
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.plots = {}
        
        # set pyplot to be interactive
        plt.ion()
        # set listeners
        self.fig.canvas.mpl_connect("close_event", self.sim.stop_running)
        # load plots
        self.load_plots(path_to_models)

    def load_plots(self, path):
        """ Loads a plot for each file on path """
        if not os.path.exists(path):
            warnings.warn("Path to plots don't exist.")
        for f in os.listdir(path):
            if f.endswith(".json"):
                f = path + "/" + f
                with open(f, "r") as rf:
                    d = json.load(rf)
                    self.add_plots(d)

    def add_plots(self, spec):
        """ Adds a plot to the class by using a dict as specification """
        if "plot" in spec:
            for i in spec["plot"]:
                model = self.sim.models[spec["name"]]
                # creating key to avoid moels with the same variable name to overide each other
                key = spec["name"] + "_" + i
                plot, = self.ax.plot(self.sim.t, getattr(model, i))
                self.plots.update({
                    key: {
                        "plot": plot,
                        "model": model,
                        "variable": i
                    }
                })

    def plot(self):
        for i in self.plots:
            plots = self.plots
            plots[i]["plot"].set_xdata(self.sim.t)
            plots[i]["plot"].set_ydata(
                getattr(plots[i]["model"], plots[i]["variable"])
            )
            self.ax.relim()
            self.ax.autoscale_view(True, True, True)
            plt.pause(0.001)

    def end(self):
        plt.ioff()
        plt.show()
        