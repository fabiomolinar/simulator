class SecondOrderFitter:
    """ Fits a second order model to given data
    
    For the open loop relationship:
    Y(s)/U(s) = [Kw^2]/[s^2+2ews+w^2]
    Where:
        Y(s) = Output
        U(s) = Input
        K = System gain
        e = Damping coefficient
        w = Natural frequency
    One can write the same thing on the time domain:
    y``+2ewy`+w^2y = Kw^2u
    Where:
        y(t) = Output
        u(t) = Input
    """
    