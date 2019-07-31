from .base import BaseModel
from ..utils.numerical_analysis import DumbDifferentiator, DumbIntegrator

class PID(BaseModel):
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
        self.D = DumbDifferentiator()
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
        error = SP - PV
        # gains
        PG = Kp*error
        IG = self.I.calculate(self.dt, error)*Kp/Ti
        DG = self.D.calculate(self.dt, error)*Kp*Td
        # output
        MV = PG + IG + DG + FWD
        # update attributes
        self.update_attributes(**{
            "error": error,
            "PG": PG,
            "IG": IG,
            "DG": DG,
            "MV": MV
        })
        return MV
        