class PID:
    """ A class used to model a PID regulator """
    def __init__(self, dt, Kp, Ti, Td, error = 0):
        # constants
        self.dt = dt
        self.Kp = [Kp]
        self.Ti = [Ti]
        self.Td = [Td]
        # state variable
        self.error = [error]
        # inputs
        self.PV = [None]
        self.SP = [None]
        # other
        self.I = [0]
        self.D = [0]
        self.PG = [0]
        self.IG = [0]
        self.DG = [0]
        # output
        self.MV = [0]


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
        