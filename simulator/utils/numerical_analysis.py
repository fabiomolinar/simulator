class DumbIntegrator:
    """ The dumbest possible numerical integrator """
    def __init__(self, m0 = 0):
        self.m0 = m0
        self.y0 = None

    def reset(self, new_m0):
        self.m0 = new_m0

    def calculate(self, dt, y):
        y0 = self.y0 if self.y0 else y
        new_area = dt*((y0 + y)/2)
        total_area = self.m0 + new_area
        # update state
        self.y0 = y
        self.m0 = total_area
        return total_area

class DumbDifferentiator:
    """ The dumbest possible numerical derivator """
    def __init__(self):
        self.y0 = None

    def calculate(self, dt, y):
        y0 = self.y0 if self.y0 else y
        rate = (y - y0)/dt
        # update state
        self.y0 = y
        return rate

class DeadBand:
    def __init__(self, db, offset = 0):
        """ Deadband with offset """
        self.db = db
        self.offset = offset

    def calculate(self, val):
        offset, db = self.offset, self.db
        if val > offset + db:
            return val - db
        if val < offset - db:
            return val + db
        return offset

