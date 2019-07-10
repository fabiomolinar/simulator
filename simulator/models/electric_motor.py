class ElectricMotor:
    """A class used to model an electric motor

    Assumptions:
        - linear magnetic circuit (not considering flux dispersions and metal saturation when high currents are applied)
        - only viscous friction is assumed to be present (not considering Coulomb frictions)
        - stator is assumed to have a single coil
        - rotor is assumed to have a single coil
    
    Source:
        - Zaccarian, L. "DC motors: dynamic model and control techniques". Available at: http://homepages.laas.fr/lzaccari/seminars/DCmotors.pdf    
    """
    def __init__(self,
                coil_turns, coil_size, magnetic_permea, solenoid_length, solenoid_area,
                stator_induc, stator_resist,
                rotor_induc, rotor_resist, rotor_inertia, viscous_friction,
                load_torque,
                stator_current, rotor_current, rotor_speed, rotor_position):
        self.N = [coil_turns]
        self.m = [magnetic_permea]
        self.l = [solenoid_length]
        self.A = [solenoid_area]
        self.d = [coil_size]
        self.K0 = self.m[-1]*self.A[-1]/self.l[-1]
        self.Kphi = self.l[-1]*self.d[-1]/self.A[-1]
        self.K = self.Kphi[-1]*self.K0[-1]*self.N[-1]
        self.Le = [stator_induc]
        self.Re = [stator_resist]
        self.Ke = 1/self.Re[-1]             # stator gain
        self.te = self.Le[-1]/self.Re[-1]   # stator time constant
        self.La = [rotor_induc]
        self.Ra = [rotor_resist]
        self.Ka = 1/self.Ra[-1]             # rotor gain
        self.ta = self.La[-1]/self.Ra[-1]   # rotor time constant
        self.J = [rotor_inertia]
        self.F = [viscous_friction]
        self.Km = 1/self.F[-1]              # mechanical gain
        self.tm = self.J[-1]/self.F[-1]     # mechanical time constant
        self.Tl = [load_torque]             # load torque exerted on the motor
        # state variables
        self.ie = [stator_current]
        self.ia = [rotor_current]
        self.w = [rotor_speed]
        self.omega = [rotor_position]
