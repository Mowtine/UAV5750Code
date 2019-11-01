import PID as PIDFile
import sys
import time
import math

from NatNetClient import NatNetClient

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
        self.frames.append([frameNumber, time.time(), trackedModelsChanged])
        self.inRecieve = True
##        print(self.frames[-1])

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
##            self.log.write("Optitrack, "+ str(uptime()) +" %4d, %4d, %4d\n"%tuple(
##                    self.position[-1]))
##            print("Received frame for rigid body", id )
##            print("Position: {} Rotation: {}".format(position,rotation))

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


valuesrc = [0,0,0,0,0,0,0]
frames   = [[0,0,0],[0,1,0],[0,2,0],[0,3,0]]
position = [[0,0,0],[0,1,0],[0,2,0],[0,3,0]]
rotation = [[0,0,0,0],[0,1,0,0],[0,2,0,0],[0,3,0,0]]
eulerAngles = [[0,0,0],[0,1,0],[0,2,0],[0,3,0]]

PID = PIDFile.PID(valuesrc,frames,position,rotation,eulerAngles, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
##vbarVal = PID.run(valuesrc,frames,position,rotation,eulerAngles);
##vbarVal = PID.run(valuesrc,frames,position,rotation,eulerAngles);
##vbarVal = PID.run(valuesrc,frames,position,rotation,eulerAngles);
vbarVal = PID.run(valuesrc,frames,position,rotation,eulerAngles);

##print(vbarVal)


valuesrc = [800, 87, 87, 87, 512, 500]
frames   = [[0,1,0],[0,2,0],[0,3,0]]
position = [[0,0,5],[2,0,0],[2,0,0]]
rotation = [[0,5,0,0],[1,0,0,0],[1,0,0,0]]
eulerAngles = [[1,0,0],[0,2,0],[0,0,0]]

# This will create a new NatNet client
optiStreamingClient = NatNetClient()
states = Optitrack(2, None)
# Configure the streaming client to call our rigid body handler on the emulator to send data out.
optiStreamingClient.newFrameListener = states.receiveNewFrame
optiStreamingClient.rigidBodyListener = states.receiveRigidBodyFrame

optiStreamingClient.run()

PID = PIDFile.PID(NormRC(valuesrc, True),frames,position,rotation,eulerAngles, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
vbarVal = PID.run(NormRC(valuesrc, True),frames,position,rotation,eulerAngles);
try:
    while True:
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

                    # frames[frameNo, systemtime, ischanged] pos[x,y,z] rot[quarts], euler[eulers
        vbarVal = PID.run(NormRC(valuesrc, True), frames, position, rotation, eulerAngles)
                    #vbarVal = PID.run(NormRC(valuesrc, True), framesT, positionT, rotationT, eulerT)
##        print(vbarVal)
        vbarVal = NormRC(vbarVal, False)
##        print(vbarVal)
##        print(vbarVal)
        sys.stdout.write(
            "%4d, %4d, %4d, %4d, %4d, %4d--------------%4f, %4f, %4f, %4f, %4f, %4f\n"%tuple(
            valuesrc[:6]+vbarVal[:6]))#+frames[-1]+position[-1]))#
                    
        sys.stdout.flush()
##        time.sleep(0.1)
except:
    optiStreamingClient.stop()
    
