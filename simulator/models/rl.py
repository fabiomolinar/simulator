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

    def reset(self):
        # state variable
        self.i = self.i[0:1]
        self.i1 = self.i1[0:1]
        # inputs
        self.Vin = self.Vin[0:1]
        # other
        self.Vr = self.Vr[0:1]
        self.Vl = self.Vl[0:1]

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

class RLLimitedVr(RL):
    """ A RL class that limits the value of Vr to a maximum value 
        by adding a dynamic resistance (Rd) in series with R.
    """
    def __init__(self, dt, resistance, inductance, current, max_Vr):
        super().__init__(dt, resistance, inductance, current)
        # constants
        self.max_Vr = [max_Vr]
        # others
        self.Rd = [None]        
        self.Vrd = [None]

    def reset(self):
        super().reset()
        # others
        self.Rd = self.Rd[0:1]        
        self.Vrd = self.Vrd[0:1]

    def calculate(self, Vin):
        i = super().calculate(Vin)
        # values for Vr < max_Vr
        Rd = 0.
        Vrd = 0.
        Vr = self.Vr[-1]
        # values if Vr > max_Vr
        max_Vr = self.max_Vr[-1]
        if Vr > max_Vr:
            Vrd = Vr - max_Vr
            Rd = Vrd/i
            # update Vr
            self.Vr[-1] = max_Vr
        # save values and return
        self.Rd.append(Rd)
        self.Vrd.append(Vrd)
        return i

        


