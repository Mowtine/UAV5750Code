import sys
import time
import threading
import socket
import pickle
from uptime import uptime
import datetime
import string
import math
#from LED import LED

#try:
#    import pigpio
#    pi = pigpio.pi()
#except Exception as e:
#    pi = None
#    print("Error connecting to pi")
#    print(e)

running = True

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

#def interrupt():
#    imp = input("Press enter to end the sim!")
#    running = False

class Optitrack:

    def __init__(self, body, log):
        self.frames = [[0, 0, 0]]
        self.position = [[0,0,0]]
        self.rotation = [[0,0,0,0]]
        self.eulerAngles = [[0,0,0]]
        self.log = log
        self.body = int(body)
        self.inRecieve = False
        self.logkeep = 200

    def GetValues(self):
        # tempframes = self.frames.copy()
        # temppos = self.position.copy()
        # temprot = self.rotation.copy()
        # tempeul = self.eulerAngles.copy()
        if len(self.frames)>self.logkeep:
            self.frames = self.frames[self.logkeep:]
        if len(self.position)>self.logkeep:
            self.position = self.position[self.logkeep:]
        if len(self.rotation)>self.logkeep:
            self.rotation = self.rotation[self.logkeep:]
        if len(self.eulerAngles)>self.logkeep:
            self.eulerAngles = self.eulerAngles[self.logkeep:]
        # self.frames = []
        # self.position = [[0,0,0]]
        # self.rotation = [[0,0,0,0]]
        # self.eulerAngles = [[0,0,0]]
        return self.frames, self.position, self.rotation, self.eulerAngles

    # This is a callback function that gets connected to the NatNet client and called once per mocap frame.
    def receiveNewFrame( self, frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        self.frames.append([frameNumber, uptime(), trackedModelsChanged])
        self.inRecieve = True
        #print(self.frames[-1])

    # This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
    def receiveRigidBodyFrame( self, id, position, rotation ):

        if self.body == id:

            self.rotation.append([float(rotation[0].real), float(rotation[1].real), float(rotation[2].real), float(rotation[3].real)])
            q0 = float(rotation[0].real)
            q1 = float(rotation[1].real)
            q2 = float(rotation[2].real)
            q3 = float(rotation[3].real)
            #print([q0,q1,q2,q3])
            #print(type(q0),type(q1),type(q2),type(q3))
            # Determine the Euler angles from the quaternions received
            theta = math.atan(((q0*q2)-(q1*q3))/(((((q0*q0)+(q1*q1)-0.5)**2)+((q1*q2+q0*q3)**2))**0.5))
            phi = math.atan((q2*q3+q0*q1)/((q0*q0)+(q3*q3)-0.5))
            psi = math.atan((q1*q2+q0*q3)/((q0*q0)+(q1*q1)-0.5))
            self.eulerAngles.append([theta, phi, psi])

            y = position[0]
            z = position[1]
            x = position[2]

            self.position.append([x, y, z])
            self.inRecieve = False
            #print(self.position[-1])
            self.log.write("Optitrack, "+ str(uptime()) +" %4d, %4d, %4d\n"%tuple(
                    self.position[-1]))
            #print("Received frame for rigid body", id )
            #print("Position: {} Rotation: {}".format(position,rotation))

def NormRC(valuestochange, norm):
    returnedVals = [0,0,0,0,0,0,0]
    if norm:
        returnedVals[0] = (valuestochange[0]-258)/(878-258)
        returnedVals[1] = (valuestochange[1]-77)/(870-77)
        returnedVals[2] = (valuestochange[2]-72)/(875-72)
        returnedVals[3] = (valuestochange[3]-77)/(875-77)
        returnedVals[4] = (valuestochange[4]-171)/(853-171)
        returnedVals[5] = (valuestochange[5]-386)/(876-386)
    else:
        returnedVals[0] = 258+(valuestochange[0])*(878-258)
        returnedVals[1] = 77+(valuestochange[1])*(870-77)
        returnedVals[2] = 72+(valuestochange[2])*(875-72)
        returnedVals[3] = 77+(valuestochange[3])*(875-77)
        returnedVals[4] = 171+(valuestochange[4])*(853-171)
        returnedVals[5] = 386+(valuestochange[5])*(876-386)

    return returnedVals



# This we only run if we are running this file
if __name__ == "__main__":

    threads = []

    body = input("Enter body number for optitrack: ")
    MyDateTime = datetime.datetime.now()
    #date = MyDateTime.isoformat()
    date = str(MyDateTime.timestamp()).split(".")[0] + str(MyDateTime.timestamp()).split(".")[1]
    logfile = open("Logs" + date + ".csv","w+")
    logfile.write("ID, Uptime, data...\n")
    #LED = LED()
    #threads.append(LED.run())
    rcInputOutput = RW.Reader("RCcontrol", logfile)
    rcInputOutput.align_serial(rcInputOutput.ser)

    try:
        # This will create a new NatNet client
        optiStreamingClient = NatNetClient()
        states = Optitrack(body, logfile)

        # Configure the streaming client to call our rigid body handler on the emulator to send data out.
        optiStreamingClient.newFrameListener = states.receiveNewFrame
        optiStreamingClient.rigidBodyListener = states.receiveRigidBodyFrame
    except:
        print("Failed to start Optitrack")
        # If we don't get OptiTrack set it as None
        optiStreamingClient = None
        states = Optitrack(body, logfile)

    groundIP = input("Enter ground station last digit: 10.0.0.")

    #try:
    #    gain = Gain.ReadGain('10.0.0.'+groundIP,5005) #designate ip address of ground station and port
    #except:
    #    gain = None
    #    print("Failed to connect to ground station")
    go = input("Ready to run?")
    try:
        threads.append(rcInputOutput.run())
        time.sleep(0.5)
        # Start up the streaming client now that the callbacks are set up.
        # This will run perpetually, and operate on a separate thread.
        threads.append(optiStreamingClient.run())
        if False:#gain:
            threads.append(gain.run())
            frames, position, rotation, eulerAngles =  states.GetValues()
            print(frames)
            print(position)
            print(rotation)
            print(eulerAngles)
            PID = PIDFile.PID(rcInputOutput.GetValues(), frames, position, rotation, eulerAngles, gain.GetValues())
        else:
            frames, position, rotation, eulerAngles =  states.GetValues()
            print(frames)
            print(position)
            print(rotation)
            print(eulerAngles)
            PID = PIDFile.PID(rcInputOutput.GetValues(), frames, position, rotation, eulerAngles, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        #gain = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        #PID.tuning("ssh conection key")
        print(" THR   AIL   ELE   RUD   GER   PIT--------------THR   AIL   ELE   RUD   GER   PIT")
        framesT = [[0,uptime(),True]]
        positionT = [[0,0,0]]
        rotationT = [[0,0,0,0]]
        eulerT = [[0,0,0]]
        logkeep = 200


        while running:
            valuesrc = rcInputOutput.GetValues()
            if valuesrc[4] < 350:
                sys.stdout.write(
                    "%4d, %4d, %4d, %4d, %4d, %4d\r"%tuple(
                    valuesrc[:6]))

                sys.stdout.flush()
                rcInputOutput.SaveValues(valuesrc)
            else:
                frames, position, rotation, eulerAngles =  states.GetValues()

                # framesT.append([framesT[-1][0]+1,uptime(),True])
                # positionT.append([0,0,0])
                # rotationT.append([0,0,0,0])
                # eulerT.append([0,0,0])
                #
                # if len(framesT)>logkeep:
                #     framesT = framesT[logkeep:]
                # if len(positionT)>logkeep:
                #     positionT = positionT[logkeep:]
                # if len(rotationT)>logkeep:
                #     rotationT = rotationT[logkeep:]
                # if len(eulerT)>logkeep:
                #     eulerT = eulerT[logkeep:]
                #print(valuesrc)

                # frames[frameNo, systemtime, ischanged] pos[x,y,z] rot[quarts], euler[eulers]
                vbarVal = PID.run(NormRC(valuesrc, True), frames, position, rotation, eulerAngles)
                #vbarVal = PID.run(NormRC(valuesrc, True), framesT, positionT, rotationT, eulerT)
                vbarVal = NormRC(vbarVal, False)
                rcInputOutput.SaveValues(vbarVal)
                sys.stdout.write(
                    "%4d, %4d, %4d, %4d, %4d, %4d--------------%4d, %4d, %4d, %4d, %4d, %4d\r"%tuple(
                    valuesrc[:6]+vbarVal[:6]))
                
                sys.stdout.flush()
            time.sleep(0.1)

    except Exception as e:
        print(e)
        logfile.close()
        for thread in threads:
            thread.exit()
            thread.join()



    finally:
        for thread in threads:
            thread.exit()
            thread.join()
        logfile.close()
