### 5/11/2019  MainDrone.py ###
# This is the main data handling function which controls all aspects of opperation. 
# The current version is ment for developer debugging, not for the final release.


import sys
import time
import threading
import socket
import pickle
from uptime import uptime
import datetime
import string
import math

# Unimplimented LED code. - It was removed because we could not fix the conflict between 
# serial ports and RPi.GPIO the Raspberry pi GPIO library. 
#from LED import LED

# Used to end the code
running = True


# Importing all other files. Filepaths can be changed depnding on folder structure. 
try:
    sys.path.insert(1, sys.path[0] + "/OptiTrack/PythonClientOptitrack/mod_python")
except:
    print("Error adding Optitrack to path")
try:
    sys.path.insert(1, sys.path[0] + "/PIDController")
except:
    print("Error adding PID to path")
try:
    sys.path.insert(1, sys.path[0] + "/ReadWriteComands")
except:
    print("Error adding RWC to path")


# Check for all imports, if a section fails to import propperly throw an error for debugging. 
try:
    lastimp = "PID"
    import PID as PIDFile
    lastimp = "Optitrack"
    from NatNetClient import NatNetClient
    lastimp = "RWC"
    import ReadWrite_Martin as RW
    lastimp = "Gain"
    import Gain as Gain
except Exception as e:
    print("Error importing: " + lastimp)
    print(e)
    exit()


# This is the Optitrack class for saving optitrack data. 
# It gives its functions to the NatNetClient's requested delegate variables
# which get called every time a frame is recieved from the NatNetClient. 
class Optitrack:

    # Initiate variables to use
    def __init__(self, body, log):
        # State list of lists
        self.frames = [[0, 0, 0]]
        self.position = [[0,0,0]]
        self.rotation = [[0,0,0,0]]
        self.eulerAngles = [[0,0,0]]
        # The log file to save data in
        self.log = log
        # Optitrack's current body
        self.body = int(body)
        self.inRecieve = False
        # Specify the max length of the list of saved optitrack data
        self.logkeep = 100

    # Give all current optitrack values
    def GetValues(self):

        # Each time values are called for it trims the lists to size
        if len(self.frames)>self.logkeep:
            self.frames = self.frames[-self.logkeep:]
        if len(self.position)>self.logkeep:
            self.position = self.position[-self.logkeep:]
        if len(self.rotation)>self.logkeep:
            self.rotation = self.rotation[-self.logkeep:]
        if len(self.eulerAngles)>self.logkeep:
            self.eulerAngles = self.eulerAngles[-self.logkeep:]

        return self.frames, self.position, self.rotation, self.eulerAngles

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    def receiveNewFrame( self, frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        
        # Append the frame number and current time for use in the PID controller. 
        self.frames.append([frameNumber, uptime(), trackedModelsChanged])
        self.inRecieve = True

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame( self, id, position, rotation ):

        if self.body == id:

            # Quartarion parsing
            q0 = float(rotation[0].real)
            q1 = float(rotation[1].real)
            q2 = float(rotation[2].real)
            q3 = float(rotation[3].real)

            # Convert to Eulers. - This origionally converted all 3 eulers
            # but was removed in speed up processing.
            t3 = 2.0*(q3*q2+q1*q0)
            t4 = 1.0 - 2.0*(q1*q1+q2*q2)
            psi = math.atan2(t3,t4)

            self.eulerAngles.append([0, psi, 0])

            y = position[0]
            x = position[1]
            z = position[2]

            self.position.append([x, y, z])
            self.inRecieve = False

            # Log data
            self.log.write("Optitrack, "+ str(uptime()) +" %4d, %4d, %4d\n"%tuple(
                    self.position[-1]))


# Function to convert between valuses recieved with the controller and 
# values to insert into the PID and back. changing norm to T/F changes the direction.
def NormRC(valuestochange, norm):
    returnedVals = [0,0,0,0,0,0,0]

    # This will beed to be "calibrated" on system start up in the future.
    if norm:
        returnedVals[0] = (valuestochange[0]-258)/(878-258)
        returnedVals[1] = (valuestochange[1]-77)/(870-77)
        returnedVals[2] = (valuestochange[2]-72)/(875-72)
        returnedVals[3] = (valuestochange[3]-77)/(875-77)
        returnedVals[4] = (valuestochange[4]-171)/(853-171)
        returnedVals[5] = (valuestochange[5]-386)/(876-386)
    else:
        returnedVals[0] = int(258+(valuestochange[0])*(878-258))
        returnedVals[1] = int(77+(valuestochange[1])*(870-77))
        returnedVals[2] = int(72+(valuestochange[2])*(875-72))
        returnedVals[3] = int(77+(valuestochange[3])*(875-77))
        returnedVals[4] = int(171+(valuestochange[4])*(853-171))
        returnedVals[5] = int(386+(valuestochange[5])*(876-386))

    return returnedVals



# This we only run if we are running this file - which in normal opperation is always
if __name__ == "__main__":

    threads = []
    
    # Ask for Optitrack body number
    body = input("Enter body number for optitrack: ")
    MyDateTime = datetime.datetime.now()
    
    # Create logfile to save data in
    date = str(MyDateTime.timestamp()).split(".")[0] + str(MyDateTime.timestamp()).split(".")[1]
    logfile = open("Logs" + date + ".csv","w+")
    logfile.write("ID, Uptime, data...\n")

    # Unimplimented LED imports
    #LED = LED()
    #threads.append(LED.run())

    try: 
        rcInputOutput = RW.Reader("RCcontrol", logfile)
        rcInputOutput.align_serial(rcInputOutput.ser)
    except Exception as e:
        print(e)
        logfile.close()
        print("Failed to connect to reciever")
        exit()


    try:
        # This will create a new NatNet client
        optiStreamingClient = NatNetClient()
        states = Optitrack(body, logfile)

        # Configure the streaming client to call our rigid body handler on the emulator to send data out.
        optiStreamingClient.newFrameListener = states.receiveNewFrame
        optiStreamingClient.rigidBodyListener = states.receiveRigidBodyFrame
    except Exception as e:
        print(e)
        print("Failed to start Optitrack")
        # If we don't get OptiTrack set it as None
        optiStreamingClient = None
        states = Optitrack(body, logfile)

    # Get the IP address for the ground station
    groundIP = input("Enter ground station last digit: 10.0.0.")

    #try:
    #    gain = Gain.ReadGain('10.0.0.'+groundIP,5005) #designate ip address of ground station and port
    #except:
    #    gain = None
    #    print("Failed to connect to ground station")

    # Break before running threads
    go = input("Ready to run?")

    try:

        # Run the reciever input thread and wait to make sure it is aligned propperly
        threads.append(rcInputOutput.run())
        time.sleep(0.5)

        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        threads.append(optiStreamingClient.run())


        # Get initial values from optitrack function
        frames, position, rotation, eulerAngles =  states.GetValues()

        gain = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        gain = [ x*10 for x in gain]
        PID = PIDFile.PID(rcInputOutput.GetValues(), frames, position, rotation, eulerAngles, gain)

        # Uncomment if manual gain pinputs are required for debugging
        #gain = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        print(" THR   AIL   ELE   RUD   GER   PIT--------------THR   AIL   ELE   RUD   GER   PIT")
        framesT = [[0,uptime(),True]]
        positionT = [[0,0,0]]
        rotationT = [[0,0,0,0]]
        eulerT = [[0,0,0]]
        logkeep = 100
        prevtime = uptime()


        while running:
            valuesrc = rcInputOutput.GetValues()

            ### Maual Mode ###
            # If in manual mode simply send the values back to the reciever function
            if valuesrc[4] < 350:
                sys.stdout.write(
                    "%4d, %4d, %4d, %4d, %4d, %4d\r"%tuple(
                    valuesrc[:6]))

                sys.stdout.flush()
                rcInputOutput.SaveValues(valuesrc)

            ### Rate Mode ###
            elif valuesrc[4] > 800:

                # Get Optitrack values
                frames, position, rotation, eulerAngles =  states.GetValues()

                # Send values from Optitrack and reciever and run a PID control loop. 
                vbarVal1 = PID.run(NormRC(valuesrc, True), frames, position, rotation, eulerAngles)

                vbarVal2 = NormRC(vbarVal1, False)

                # Save updated control values for writing to the copter
                rcInputOutput.SaveValues(vbarVal2)
                sys.stdout.write(
                    "%4d, %4d, %4d, %4d, %4d, %4d--------------%4d, %4d, %4d, %4d, %4d, %4d\r"%tuple(
                    valuesrc[:6]+vbarVal2[:6]))
                sys.stdout.flush()

            # Sleep to allow other threads to run
            time.sleep(0.008)

    except Exception as e:
        print(e)
        logfile.close()
        optiStreamingClient.stop()
