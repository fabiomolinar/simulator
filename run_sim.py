import matplotlib.pyplot as plt
from models.signal_generator import signal_generator
from models.rc import rc

def run(duration, dt):
    running = True
    # initial values
    volt = [10]
    charge = [0]
    t = [0]
    cycles = int(duration/dt)
    sig = signal_generator(
        [
            {
                "start": {
                    "value":volt[0]
                }
            },
            {
                "step": {
                    "cycle": 10000,
                    "value": 5
                }
            },
            {
                "step": {
                    "cycle": 30000,
                    "value": 15
                }
            },
            {
                "ramp_down": {
                    "cycle": 40000,
                    "value": 0.001
                }
            }
        ]
    )
    circuit = rc(dt, 10, 1, charge[0])

    # set pyplot to be interactive
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    volt_line, = ax.plot(t, volt, '-r')
    charge_line, = ax.plot(t, charge, '-b')

    # set listeners
    def stop_running(self):
        nonlocal running
        running = False
    fig.canvas.mpl_connect("close_event", stop_running)
    
    # loop
    for i in range(cycles):
        if not running:
            break
        # update time
        t.append(t[-1:][0] + dt)
        volt.append(sig.calculate(i))
        charge.append(circuit.calculate(volt[-1:][0]))

        # update plot every 0.5 seconds
        if i % (2/dt) == 0.0:
            volt_line.set_xdata(t)
            volt_line.set_ydata(volt)
            charge_line.set_xdata(t)
            charge_line.set_ydata(charge)
            ax.relim()
            ax.autoscale_view(True, True, True)
            plt.pause(0.001)
    
    # at the end, keep plot open
    plt.ioff()
    plt.show()
    print("finished")
    
if __name__ == "__main__":
    run(60, 0.001)
    