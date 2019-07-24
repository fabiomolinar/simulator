import os
import warnings
import json
import matplotlib.pyplot as plt
from ..settings import simulator_settings
from  .line import Line

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
        self.plots.update(self.load_plots(path_to_models))
        # plot settings
        plt.title("My small simulator")
        plt.xlabel("time [s]")
        self.ax.legend()

    def load_plots(self, path):
        """ Loads a plot for each file on path """
        if not os.path.exists(path):
            warnings.warn("Path to plots don't exist.")
            return {}
        plots = {}
        for f in os.listdir(path):
            if f.endswith(".json"):
                f = path + "/" + f
                with open(f, "r") as rf:
                    d = json.load(rf)
                    plots.update(self.add_plots(d))
        return plots

    def add_plots(self, spec):
        """ Adds a plot to the class by using a dict as specification """
        plots = {}
        if "plot" in spec:
            for i in spec["plot"]:
                model = self.sim.models[spec["name"]]
                line = Line(model, i, spec["plot"][i])
                # creating key to avoid moels with the same variable name to overide each other
                key = spec["name"] + "_" + i
                label = self.create_legend(spec, i)
                # fill plot with first values
                plot, = self.ax.plot(self.sim.t, line.get_values(), label=label)
                plots.update({
                    key: {
                        "plot": plot,
                        "line": line
                    }
                })
        return plots

    def create_legend(self, spec, el):
        label = spec["plot"][el]["legend"] if "legend" in spec["plot"][el] else el
        if "multiplier" in spec["plot"][el]:
            label = label + " [x{}]".format(spec["plot"][el]["multiplier"])
        return label

    def plot(self):
        # Update values
        for i in self.plots:
            self.plots[i]["plot"].set_xdata(self.sim.t)
            self.plots[i]["plot"].set_ydata(self.plots[i]["line"].get_values())
        # Update plot
        self.ax.relim()
        self.ax.autoscale_view(True, True, True)
        plt.pause(0.001)

    def end(self):
        # Remove interactive mode but keeps plot opened
        plt.ioff()
        plt.show()
        