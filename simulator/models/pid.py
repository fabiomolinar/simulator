class PID:
    """ A class used to model a PID regulator """
    def __init__(self, dt, Kp, Ti, Td, I0, D0):
        # constants
        self.dt = dt
        self.Kp = [Kp]
        self.Ti = [Ti]
        self.Td = [Td]
        # state variable
        self.I = [I0]
        self.I1 = [I0]
        self.D = [D0]
        self.D1 = [D0]
        # inputs
        self.PV = [None]
        self.SP = [None]
        # other
        self.error = [None]
        self.MV = [None]
        self.P = [None]


    def calculate(self, SP, PV, FWD):
        """ Calculates the next value and adds it to the memory """
        Kp = self.Kp[-1]
        Ti = self.Ti[-1]
        Td = self.Td[-1]
        # error
        self.error.append(SP - PV)
        # gains
        self.P.append(Kp*self.error[-1])
        self.I.append(self.I1[-1] + self.dt*self.error[-1])
        self.I1.append(self.I[-1])
        