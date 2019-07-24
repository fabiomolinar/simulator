class RL:
    """ A class used to model an RL (resistor-inductor) circuit """
    def __init__(self, dt, resistance, inductance, current):
        # constants
        self.dt = dt
        self.R = [resistance]
        self.L = [inductance]
        # state variable
        self.i = [current]
        self.i1 = [current]
        # inputs
        self.Vin = [None]
        # other
        self.Vr = [None]
        self.Vl = [None]

    def calculate(self, Vin):
        """ Calculates the next value and adds it to the memory """
        self.Vr.append(self.i[-1]*self.R[-1])
        self.Vl.append(Vin - self.Vr[-1])
        # update state variables
        self.i.append(self.dt*self.Vl[-1]/self.L[-1] + self.i1[-1])
        self.i1.append(self.i[-1])
        # save input just for recording
        self.Vin.append(Vin)
        # return the current
        return self.i[-1]