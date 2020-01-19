import numpy as np

class SecondOrderFitter:
    """ Fits a second order model to given data

    Args:
        data (ndarray): list with data on the measured time (optional), inputs and outputs
            items:
                time (float): in seconds
                input (float)
                output (float)
        dt (float): time difference between measured points (if time information isn't given) in seconds
    """

    def __init__(self, data, dt = None):
        # Check if inputs are valid
        self.inputs_are_valid(data, dt)
        # store inputs
        self.raw_data = data
        self.dt = dt
        self.data = self.prepare_data(data, dt)
    
    def model(t, y, u, k, e, w):
        """Model of a second order system
        
        For the open loop relationship: Y(s)/U(s) = [Kw^2]/[s^2+2ews+w^2]
        One can write the same thing on the time domain:
        y''+2ewy'+w^2y = Kw^2u
        Defining the state variables:
            x1 = y
            x2 = y'
        The following state equations can be defined:
            x1' = x2
            x2' = Kw^2u - (2ewx2+w^2x1)

        Args:
            t (float): time
            y (list of floats): outputs
            u (float): inputs
            k (float): system gain
            e (float): damping coefficient
            w (float): natural frequency

        Returns:
            x (list of floats): states
        """
        x = np.zeros(2)
        x[0] = 


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