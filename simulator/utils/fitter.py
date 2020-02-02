from abc import ABC, abstractstaticmethod, abstractmethod
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

class Fitter(ABC):
    """ Fits a model to given data

    Args:
        data (ndarray): list with data on the measured time (optional), inputs and outputs
            items:
                time (float): in seconds
                input (float)
                output (float)
        p0 (list): list with initial guesses for parameters
        dt (float): time difference between measured points (if time information isn't given) in seconds
    """

    def __init__(self, data, p0, dt = None):
        # Check if inputs are valid
        self.inputs_are_valid(data, dt)
        self.parameters_are_valid(p0)
        # Store inputs
        self.raw_data = data
        self.dt = dt
        self.data = self.prepare_data(data, dt)
        # Store initial guesses
        self.p0 = p0
        # Optimization results
        self.success = None
        self.message = None
    
    @abstractstaticmethod
    def model(t, x, u, p):
        """Model of a system
                
        Args:
            t (float): time
            x (list of floats): states
            u (float): inputs
            p (list): list of parameters

        Returns:
            dx (list of floats): states derivatives
        """
        pass

    def integrate(self, p):
        """Function used to simulate a system given a list of parameters"""
        lines = self.data.shape[0]
        y = np.zeros(lines)
        y[0] = self.data[0,2]
        # Considering that at initial state the system is stable (y' = 0)
        x0 = [y[0], 0.0]
        for line in range(1,lines):
            x = solve_ivp(
                self.model,
                (self.data[line-1,0], self.data[line,0]),
                x0,
                args = (self.data[line,1], p)
            )
            # Update state
            x0 = x.y[:,-1]
            y[line] = x.y[0,-1]
        return y

    def objective(self, p):
        """Cost function used to evaluate the system against given data"""
        y = self.integrate(p)
        obj = 0
        for index, value in enumerate(y):
            obj += (value-self.data[index,2])**2
        return obj
    
    @abstractmethod
    def fit(self, p0 = None):
        """Search for the parameters that better minimize the objective function"""
        pass

    def prepare_data(self, data, dt):
        """Create the correct data structure that will be used by the class
        
        The first column represents time in seconds since the epoch and should be of type float
        The second column represents the inputs and should be of type float
        The third column represents the outputs and should be of type float
        """
        col_number = data.shape[1]
        if col_number >= 3:
            return data[:, 0:3]
        if col_number == 2:
            lines = data.shape[0]
            time = np.linspace(0, dt*(lines-1), lines)
            return np.column_stack((time, data))
    
    def inputs_are_valid(self, data, dt):
        """Checks if the given inputs to the class are valid
        
        This class don't return anything. It simply raises
        and error if there is one.
        """
        # Data has to be an numpy.ndarray
        if type(data) is not np.ndarray:
            raise TypeError("Argument data has to be of numpy.ndarray type.")
        # Data has to be of type float
        if data.dtype is not np.dtype("float64"):
            raise TypeError("Argument data should be of type float.")
        col_number = data.shape[1]
        # There has to be at least 2 columns
        if col_number < 2:
            raise ValueError("Argument data has to have at least 2 columns.")
        # If there are only 2 columns, then time information has to be given
        if col_number == 2 and type(dt) is not float:
            raise TypeError("Argument dt has to be a float.")
        # When using dt, it can't be less than 0
        if col_number == 2 and dt <= 0.0:
            raise ValueError("Argument dt has to be greater than 0.")
        # When time is provided, make sure it is in ascending order
        if col_number >= 3:
            # Check the first column (time) is in ascending order
            lines = data.shape[0]
            for i in range(lines):
                if i == 0:
                    continue
                if data[i,0] <= data[i-1,0]:
                    raise ValueError("The time column needs to be in ascending order")

    @staticmethod
    def parameters_are_valid(p0):
        pass

class FitterWithInputDelay(Fitter):
    """Class used for models whose model take an input with time delay
    
    The time delay is created at the `integrate` method by interpolating
    the list of time and inputs with a newly calculated delayed time.
    """

    def integrate(self, p):
        """Function used to simulate a system given a list of parameters
        
        Additionally, this function also creates a new input u to the 
        model which is a delayed input calculated using interpolation.

        This function consider that the time delay parameter is the 
        last parameter given by the `p` argument. In other words:
            time delay setting = p[-1]
        """
        lines = self.data.shape[0]
        y = np.zeros(lines)
        y[0] = self.data[0,2]
        # Considering that at initial state the system is stable (y' = 0)
        x0 = [y[0], 0.0]
        for line in range(1,lines):
            # Delay input calculated through interpolation
            t = self.data[line-1,0]
            the = p[-1]
            delayed_time = t - the
            func_u = interp1d(
                self.data[:,0],self.data[:,1],
                bounds_error=False, fill_value=(self.data[0,1], self.data[lines-1,1])
            )
            u = func_u(delayed_time)
            # integrate
            x = solve_ivp(
                self.model,
                (t, self.data[line,0]),
                x0,
                args = (u, p[0:-1])
            )
            # Update state
            x0 = x.y[:,-1]
            y[line] = x.y[0,-1]
        return y

class FirstOrderFitter(Fitter):
    """Fits a first order model to given data
    
    Args:
        p0:
            k (float): system gain
            t (float): time constant
    """

    def __init__(self, data, p0, dt = None):
        super().__init__(data, p0, dt)
        # Calculated parameters of the FOF
        self.k = None
        self.t = None

    @staticmethod
    def model(t, x, u, p):
        """Model of a first order system
        
        For the open loop relationship: Y(s)/U(s) = K/[Ts+1]
        One can write the same thing on the time domain:
        Ty' + y = Ku
        Defining the state variables:
            x0 = y
        The following state change equations can be defined:
            x0' = (Ku-x0)/T
        
        Args:
            t (float): time
            x (list of floats): states
            u (float): inputs
            p (list): list of parameters
                k (float): system gain
                tc (float): time constant

        Returns:
            dx (list of floats): states derivatives
        """
        # Unpack parameters
        k, tc = p
        # Unpack initial conditions
        x0 = x
        # Calculate derivatives
        dx = np.zeros(1)
        dx = (k*u - x0)/tc
        return dx

    def fit(self, p0 = None):
        """Search for the parameters that better minimize the objective function"""
        if not p0:
            p0 = self.p0
        else:
            self.parameters_are_valid(p0)
        result = minimize(self.objective, p0, bounds=[
            (None, None),
            (0, None)
        ])
        self.k, self.t = result.x
        self.success = result.success
        self.message = result.message
        return result.success

    @staticmethod
    def parameters_are_valid(p0):
        k, t = p0
        if t < 0:
            raise ValueError("Time constant can't be negative.")

class FirstOrderPlusDeadTimeFitter(FitterWithInputDelay, FirstOrderFitter):
    """Fits a first order model with dead time to given data
    
    Args:
        p0:
            k (float): system gain
            t (float): time constant
            the (float): dead time
    """

    def __init__(self, data, p0, dt = None):
        super().__init__(data, p0, dt)
        # Calculated parameters of the FOF
        self.k = None
        self.t = None
        self.the = None

    def fit(self, p0 = None):
        """Search for the parameters that better minimize the objective function"""
        if not p0:
            p0 = self.p0
        result = minimize(self.objective, p0, bounds=[
            (None, None),
            (0, None),
            (0, None)
        ])
        self.k, self.t, self.the = result.x
        self.success = result.success
        self.message = result.message
        return result.success
        
class SecondOrderFitter(Fitter):
    """ Fits a second order model to given data
    
    Args:
        p0:
            k (float): system gain
            e (float): damping coefficient
            w (float): natural frequency
    """

    def __init__(self, data, p0, dt = None):
        super().__init__(data, p0, dt)
        # Calculated parameters of the SOF
        self.k = None
        self.e = None
        self.w = None
    
    @staticmethod
    def model(t, x, u, p):
        """Model of a second order system
        
        For the open loop relationship: Y(s)/U(s) = [Kw^2]/[s^2+2ews+w^2]
        One can write the same thing on the time domain:
        y''+2ewy'+w^2y = Kw^2u
        Defining the state variables:
            x0 = y
            x1 = y'
        The following state change equations can be defined:
            x0' = x1
            x1' = Kw^2u - (2ewx1+w^2x0)
        
        Args:
            t (float): time
            x (list of floats): states
            u (float): inputs
            p (list): list of parameters
                k (float): system gain
                e (float): damping coefficient
                w (float): natural frequency

        Returns:
            dx (list of floats): states derivatives
        """
        # Unpack parameters
        k, e, w = p
        # Unpack initial conditions
        x0, x1 = x
        # Calculate derivatives
        dx = np.zeros(2)
        dx[0] = x1
        dx[1] = k*w**2*u - (2*e*w*x1 + w**2*x0)
        return dx

    def fit(self, p0 = None):
        """Search for the parameters that better minimize the objective function"""
        if not p0:
            p0 = self.p0
        else:
            self.parameters_are_valid(p0)
        result = minimize(self.objective, p0, bounds=[
            (None, None),
            (0, None),
            (0, None)
        ])
        self.k, self.e, self.w = result.x
        self.success = result.success
        self.message = result.message
        return result.success

    @staticmethod
    def parameters_are_valid(p0):
        k, e, w = p0
        if e < 0:
            raise ValueError("Damping coefficient can't be negative.")
        if w < 0:
            raise ValueError("Natural frequency can't be negative.")

class SecondOrderPlusDeadTimeFitter(FitterWithInputDelay, SecondOrderFitter):
    """ Fits a second order model to given data
    
    Args:
        p0:
            k (float): system gain
            e (float): damping coefficient
            w (float): natural frequency
            the (float): dead time
    """

    def __init__(self, data, p0, dt = None):
        super().__init__(data, p0, dt)
        # Calculated parameters of the FOF
        self.k = None
        self.e = None
        self.w = None
        self.the = None

    def fit(self, p0 = None):
        """Search for the parameters that better minimize the objective function"""
        if not p0:
            p0 = self.p0
        result = minimize(self.objective, p0, bounds=[
            (None, None),
            (0, None),
            (0, None),
            (0, None)
        ])
        self.k, self.e, self.w, self.the = result.x
        self.success = result.success
        self.message = result.message
        return result.success