class PID:

    # Discrete PID control

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        # Update Gain Values
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator

	# Anti-Wind-Up Thresholds
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min

        self.set_point=0.0
        self.error=0.0

    def update(self,current_value,P=2.0,I=0.0,D=1.0,Imax=500,Imin=-500):

        # Update PID Gains
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Integrator_max=Imax
        self.Integrator_min=Imin

	# Calculate PID output value for given reference input and feedback

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

        #print(self.P_value)
        #print(self.I_value)
        #print(self.D_value)

        return PID

    def setPoint(self,set_point):

	# Initilize the setpoint of PID
        self.set_point = set_point
        #self.Integrator=0
        #self.Derivator=0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator

def PIDLoop():

    while True :

        # Get Target Values and Sensor Values from Communication
        X_Target_Value = 5.0
        Y_Target_Value = 5.0
        Z_Target_Value = 5.0
        Psi_Target_Value = 10.0

        X_Sensor_Value = 4.0
        Y_Sensor_Value = 4.0
        Z_Sensor_Value = 4.0
        Psi_Sensor_Value = 9.0

        u_Sensor_Value = 14.0
        v_Sensor_Value = 14.0
        w_Sensor_Value = 14.0
        r_Sensor_Value = 14.0
        #

        # Get Gain Values from Tuning UI
        KP = [2.0]*8
        KI = [1.0]*8
        KD = [0.0]*8
        Imax = [100.0]*8
        Imin = [-100.0]*8
        #

        # PID Discrete Control
        X.setPoint(X_Target_Value)
        Y.setPoint(Y_Target_Value)
        Z.setPoint(Z_Target_Value)
        Psi.setPoint(Psi_Target_Value)

        u_Target_Value = X.update(X_Sensor_Value,KP[0],KI[0],KD[0],Imax[0],Imin[0])
        v_Target_Value = Y.update(Y_Sensor_Value,KP[1],KI[1],KD[1],Imax[1],Imin[1])
        w_Target_Value = Z.update(Z_Sensor_Value,KP[2],KI[2],KD[2],Imax[2],Imin[2])
        r_Target_Value = Psi.update(Psi_Sensor_Value,KP[3],KI[3],KD[3],Imax[3],Imin[3])

        u.setPoint(u_Target_Value)
        v.setPoint(v_Target_Value)
        w.setPoint(w_Target_Value)
        r.setPoint(r_Target_Value)

        u_Control = u.update(u_Sensor_Value,KP[4],KI[4],KD[4],Imax[4],Imin[4])
        v_Control = v.update(v_Sensor_Value,KP[5],KI[5],KD[5],Imax[5],Imin[5])
        w_Control = w.update(w_Sensor_Value,KP[6],KI[6],KD[6],Imax[6],Imin[6])
        r_Control = r.update(r_Sensor_Value,KP[7],KI[7],KD[7],Imax[7],Imin[7])
        print(u_Control)

        #

################################################################################
                                #       Main Loop      #
################################################################################

# Load Tuning UI

#
if __name__ == "__main__":
    # Call PID class def for State Controller
    X   =PID(3.0,0.4,0.8,0,0)
    Y   =PID(3.0,0.4,0.8,0,0)
    Z   =PID(3.0,0.4,0.8,0,0)
    Psi =PID(3.0,0.4,0.8,0,0)
    u   =PID(3.0,0.4,0.8,0,0)
    v   =PID(3.0,0.4,0.8,0,0)
    w   =PID(3.0,0.4,0.8,0,0)
    r   =PID(3.0,0.4,0.8,0,0)
    print('Initialized')

    [u_C,v_C,w_C,r_C] = PIDLoop()
