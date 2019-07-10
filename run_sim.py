import matplotlib.pyplot as plt
from simulator.simulator import Simulator
from simulator.settings import simulator_settings
from simulator.models.signal_generator import SignalGenerator
from simulator.models.rc import RC

def run(duration, dt):
    sim = Simulator(simulator_settings["path_to_models"], dt, duration)

    # set pyplot to be interactive
    """
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    volt_line, = ax.plot(sim.t, volt, '-r')
    charge_line, = ax.plot(sim.t, charge, '-b')
    """

    # set listeners
    """
    def stop_running(self, sim):
        sim.stop_running()
    fig.canvas.mpl_connect("close_event", stop_running)
    """
    
    # loop
    sim.run()
    
    # at the end, keep plot open
    """
    plt.ioff()
    plt.show()
    print("finished")
    """
    
if __name__ == "__main__":
    run(60, 0.001)
    