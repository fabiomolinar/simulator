from .base import BaseModel
from ..utils.numerical_analysis import DumbDifferentiator, DumbIntegrator

class PID(BaseModel):
    """A class used to model the most simple PID regulator possible.

    Args:
        dt (float): cycle time
        Kp (float): proportional gain
        Ti (float): integral time
        Td (float): derivative time
        error (float): initial value given to the
            state variable error
    """
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
        """Calculates the next value and adds it to the memory."""
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
    """PID regulator with limited MV

    A class that simulates a PID regulator 
    with limited MV settings.
    This is a dumb PID script since it only limits
    MV, but it does nothing to the gains themselves.

    Args:
        min_MV (float): lower limit value for calculated MV.
            If None is given, no limit is applied.
        max_MV (float): upper limit value for calculated MV.
            If None is given, no limit is applied.
    """
    def __init__(self, dt, Kp, Ti, Td, error = 0, 
                 min_MV = None, max_MV = None):
        super().__init__(dt, Kp, Ti, Td, error)
        # settings
        self.min_MV = [min_MV]
        self.max_MV = [max_MV]

    def calculate(self, SP, PV, FWD):
        MV = super().calculate(SP, PV, FWD)
        max_MV = self.max_MV[-1]
        min_MV = self.min_MV[-1]
        # limit MV
        if max_MV and MV > max_MV:
            self.MV[-1] = max_MV
            return max_MV
        if min_MV and MV < min_MV:
            self.MV[-1] = min_MV
            return min_MV
        return MV

class PIDLimitedIntegral(PIDLimitedMV):
    """Improved PID implementation 

    Args:
        min_integral (float): lower limit value for the integral action.
        max_integral (float): upper limit value for the integral action.
        db_derivative (bool): deadband applied to the derivative action.
    """
    def __init__(self, dt, Kp, Ti, Td, error = 0, 
                 min_MV = None, max_MV = None, 
                 min_integral = None, max_integral = None, 
                 db_derivative = 0, differ_on_PV = True):
        super().__init__(self, dt, Kp, Ti, Td, error, min_MV, max_MV)
        # settings
        self.min_integral = [self.set_min_integral(min_integral)]
        self.max_integral = [self.set_max_integral(max_integral)]
        self.db_derivative = [db_derivative]
        self.differ_on_PV = [differ_on_PV]

    def set_min_integral(self, min_integral):
        min_MV = self.min_MV
        if min_MV and min_integral and min_integral < min_MV:
            return min_MV
        return min_integral

    def set_max_integral(self, max_integral):
        max_MV = self.max_MV
        if max_MV and max_integral and max_integral > max_MV:
            return max_MV
        return max_integral
