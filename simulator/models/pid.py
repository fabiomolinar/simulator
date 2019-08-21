from .base import BaseModel
from ..utils.numerical_analysis import DumbDifferentiator, DumbIntegrator

class PID(BaseModel):
    """ A class used to model the most simple PID regulator possible """
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
        
class PIDLimitedMV(PID):
    """ A class that simulates a PID regulator 
        with limited MV settings.
        This is a dumb PID script since it only limits
        MV, but it does nothing to the gains themselves.
    """
    def __init__(self, dt, Kp, Ti, Td, error = 0, min_MV = None, max_MV = None):
        super().__init__(dt, Kp, Ti, Td, error)
        # settings
        self.min_MV = [min_MV]
        self.max_MV = [max_MV]

    def calculate(self, SP, PV, FWD):
        MV = super().calculate(SP, PV, FWD)
        max_MV = self.max_MV[-1]
        min_MV = self.min_MV[-1]
        # limit MV
        if MV > max_MV:
            self.MV[-1] = max_MV
            return max_MV
        if MV < min_MV:
            self.MV[-1] = min_MV
            return min_MV
        return MV

