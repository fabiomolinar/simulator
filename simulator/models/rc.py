class RC:
    """A class used to model an RC (resistor-capacitor) circuit"""
    def __init__(self, dt, resistance, capacitance, charge):
        # constants
        self.dt = dt
        self.R = resistance
        self.C = capacitance
        # state variable
        self.Q = charge
        self.Q1 = charge
        # inputs
        self.Vin = None
        # other
        self.Vr = None
        self.Vc = None
        self.i = None        

    def calculate(self, Vin):
        self.Vc = self.Q/self.C
        self.Vr = Vin - self.Vc
        self.i = self.Vr/self.R
        # update state variables
        self.Q = self.dt*((1/self.R)*(Vin-(1/self.C)*self.Q1))+self.Q1
        self.Q1 = self.Q
        # save input just for recording
        self.Vin = Vin
        # return the current
        return self.Q