from simulator.simulator import Simulator
from simulator.settings import simulator_settings
from simulator.models.signal_generator import SignalGenerator
from simulator.models.rc import RC
from simulator.plots.plot import Plot
from simulator.utils.performance_meter import PerformanceMeter

def run():
    duration = simulator_settings["duration"]
    dt = simulator_settings["dt"]
    sim = Simulator(simulator_settings["path_to_models"], dt, duration)
    plot, pf = None, None
    if simulator_settings["show_plot"]:
        plot = Plot(simulator_settings["path_to_models"], sim)
    if simulator_settings["performance_meter"]:
        if simulator_settings["performance_meter"]["enabled"]:
            pf = PerformanceMeter(sim, simulator_settings["performance_meter"])
    # loop
    sim.run(plot, pf)
    
if __name__ == "__main__":
    run()