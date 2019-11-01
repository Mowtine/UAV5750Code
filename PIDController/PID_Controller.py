class PID_Controller:
    # Discrete PID control
    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
        # Gain Values
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator
	# Anti-Wind-Up Thresholds
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min
        self.set_point=0.0

    def update(self,current_value,P=2.0,I=0.0,D=1.0,Imax=500,Imin=-500):
        # Update PID Gains
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Integrator_max=Imax
        self.Integrator_min=Imin

	# Calculate PID output value for given reference input and feedback
        #
        #print(self.set_point)
        # print(current_value)
        self.error = self.set_point - current_value
        self.P_value = self.Kp * self.error

        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min
        self.I_value = self.Integrator * self.Ki

        PID = self.P_value + self.I_value + self.D_value
        # print(self.P_value)
        return PID

    def setPoint(self,set_point):
        self.set_point = set_point
