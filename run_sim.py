from simulator.simulator import Simulator
from simulator.settings import simulator_settings
from simulator.models.signal_generator import SignalGenerator
from simulator.models.rc import RC
from simulator.plots.plot import Plot

def run(duration, dt):
    sim = Simulator(simulator_settings["path_to_models"], dt, duration)
    if simulator_settings["show_plot"]:
        plot = Plot(simulator_settings["path_to_models"], sim)
    # loop
    sim.run(plot)
    
if __name__ == "__main__":
    run(2.0, 0.001)