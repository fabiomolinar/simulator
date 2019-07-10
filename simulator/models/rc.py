class RC:
    """A class used to model an RC (resistor-capacitor) circuit"""
    def __init__(self, dt, resistance, capacitance, charge):
        # constants
        self.dt = dt
        self.R = [resistance]
        self.C = [capacitance]
        # state variable
        self.Q = [charge]
        self.Q1 = [charge]
        # inputs
        self.Vin = [None]
        # other
        self.Vr = [None]
        self.Vc = [None]
        self.i = [None]        

    def calculate(self, Vin):
        self.Vc.append(self.Q[-1]/self.C[-1])
        self.Vr.append(Vin - self.Vc[-1])
        self.i.append(self.Vr[-1]/self.R[-1])
        # update state variables
        self.Q.append(self.dt*((1/self.R[-1])*(Vin-(1/self.C[-1])*self.Q1[-1]))+self.Q1[-1])
        self.Q1.append(self.Q[-1])
        # save input just for recording
        self.Vin.append(Vin)
        # return the current
        return self.Q[-1]