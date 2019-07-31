from ..utils.numerical_analysis import DumbDerivator, DumbIntegrator

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
        self.I = DumbIntegrator()
        self.D = DumbDerivator()
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
        # gains
        self.PG.append(Kp*self.error[-1])
        self.IG.append((Kp/Ti)*self.I.calculate(self.dt, self.error[-1]))
        self.DG.append(Kp*Td*self.D.calculate(self.dt, self.error[-1]))
        # output
        MW = self.PG[-1] + self.IG[-1] + self.DG[-1] + FWD
        self.MV.append(MW)
        return MW
        