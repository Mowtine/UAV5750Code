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
        
        # PID Discrete Control
        X.setPoint(X_Target_Value)
        Y.setPoint(Y_Target_Value)
        Z.setPoint(Z_Target_Value)
        Psi.setPoint(Psi_Target_Value)
        
        u_Target_Value = X.update(X_Sensor_Value)
        v_Target_Value = Y.update(Y_Sensor_Value)
        w_Target_Value = Z.update(Z_Sensor_Value)
        r_Target_Value = Psi.update(Psi_Sensor_Value)
        
        u.setPoint(u_Target_Value)
        v.setPoint(v_Target_Value)
        w.setPoint(w_Target_Value)
        r.setPoint(r_Target_Value)
        
        u_Control = u.update(u_Sensor_Value)
        v_Control = v.update(v_Sensor_Value)
        w_Control = w.update(w_Sensor_Value)
        r_Control = r.update(r_Sensor_Value)
        #
