class electric_motor:
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
        self.N = coil_turns
        self.m = magnetic_permea
        self.l = solenoid_length
        self.A = solenoid_area
        self.d = coil_size
        self.K0 = self.m*self.A/self.l
        self.Kphi = self.l*self.d/self.A
        self.K = self.Kphi*self.K0*self.N
        self.Le = stator_induc
        self.Re = stator_resist
        self.Ke = 1/self.Re             # stator gain
        self.te = self.Le/self.Re       # stator time constant
        self.La = rotor_induc
        self.Ra = rotor_resist
        self.Ka = 1/self.Ra             # rotor gain
        self.ta = self.La/self.Ra       # rotor time constant
        self.J = rotor_inertia
        self.F = viscous_friction
        self.Km = 1/self.F              # mechanical gain
        self.tm = self.J/self.F         # mechanical time constant
        self.Tl = load_torque           # load torque exerted on the motor
        # state variables
        self.ie = stator_current
        self.ia = rotor_current
        self.w = rotor_speed
        self.omega = rotor_position
