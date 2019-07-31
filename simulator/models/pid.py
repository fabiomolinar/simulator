class PID:
    """ A class used to model a PID regulator """
    def __init__(self, dt, Kp, Ti, Td, error0 = 0):
        # constants
        self.dt = dt
        self.Kp = [Kp]
        self.Ti = [Ti]
        self.Td = [Td]
        # state variable
        self.error = [error0]
        # inputs
        self.PV = [None]
        self.SP = [None]
        # other
        self.I = [None]
        self.D = [None]
        self.PG = [None]
        self.IG = [None]
        self.DG = [None]
        # output
        self.MV = [None]


    def calculate(self, SP, PV, FWD):
        """ Calculates the next value and adds it to the memory """
        Kp = self.Kp[-1]
        Ti = self.Ti[-1]
        Td = self.Td[-1]
        # error
        self.error.append(SP - PV)
        # integral and derivative parts
        self.I.append(self.I[-1] + self.dt*((self.error[-1] + self.error[-2])/2))
        self.D.append((self.error[-1] - self.error[-2])/(self.dt))
        # gains
        self.PG.append(Kp*self.error[-1])
        self.IG.append((Kp/Ti)*self.I[-1])
        self.DG.append(Kp*Td*self.D[-1])
        # output
        MW = self.PG[-1] + self.IG[-1] + self.DG[-1] + FWD
        self.MV.append(MW)
        return MW
        