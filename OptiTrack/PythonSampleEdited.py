#
# Uses the Python NatNetClient.py library to establish a connection (by creating a NatNetClient),
# and receive data via a NatNet connection and decode it using the NatNetClient library.

# Load the math library to allow trigonometric functions to be used below
import math

from NatNetClient import NatNetClient

# This is a callback function that gets connected to the NatNet client and called once per mocap frame.
def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):

    print( "Received frame", frameNumber )

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receiveRigidBodyFrame( id, position, rotation ):


    # THE FOLLOWING CODE TO BE IMPLEMENTED OUTSIDE OF THIS FUNCTION SO THAT THE VARIABLES MAY BE STORED PER ITERATION (required to determine rates)
    # The following is only for body position and rotation rates, if an LVLH frame is required will need a DCM (confirm with Brian whether optitrack records body or local values)

        # POSITION SECTION
        # Break the functions variables into more user friendly variables to perform the required calculations
        q0 = rotation[0]
        q1 = rotation[1]
        q2 = rotation[2]
        q3 = rotation[3]

        # Break the position vector into its individual variables (may need to swap the y and z axes CONFIRM WITH BRIAN)
        x = position[0]
        y = position[1]
        z = position[2]

        # Define the timestamp and store for every iteration
        dt = timestamp

        # Determine the Euler angles from the quaternions received
        theta = math.atan(((q0*q2)-(q1*q3))/(((((q0*q0)+(q1*q1)-0.5)**2)+((q1*q2+q0*q3)**2))**0.5))
        phi = math.atan((q2*q3+q0*q1)/((q0**q0)+(q3**q3)-0.5))
        psi = math.atan((q1*q2+q0*q3)/((q0**q0)+(q1**q1)-0.5))

        # RATES SECTION
        ## Now assume that values have been stored in the next iteration (TO CHECK WITH MARTIN HOW TO DO OUTSIDE OF THIS FUNCTION)
        # Create two seperate arrays to store the rates data
        posrates = np.ones(len(position))
        rotrates = np.ones(len(rotation))

        # assume an array exists with x2 and x1 stored (new timestep and previous timestep values)
        posrates[0] = (x2-x1)/(dt)
        posrates[1] = (y2-y1)/(dt)
        posrates[2] = (z2-z1)/(dt)
        rotrates[0] = (q0_2-q0_1)/(dt)
        rotrates[1] = (q1_2-q1_1)/(dt)
        rotrates[2] = (q2_2-q2_1)/(dt)
        rotrates[3] = (q3_2-q3_1)/(dt)

        # p,q,r are rotation rates about the body frame (the euler angle rates (rotrates array)); if optitrack isn't in the local body axis then DCM to convert and then will equal to the euler angle rates

        # will need to incorporate an IF statement at the start to account for when position isnt recorded for that framenumber



# This will create a new NatNet client
streamingClient = NatNetClient()

# Configure the streaming client to call our rigid body handler on the emulator to send data out.
streamingClient.newFrameListener = receiveNewFrame
streamingClient.rigidBodyListener = receiveRigidBodyFrame

# Start up the streaming client now that the callbacks are set up.
# This will run perpetually, and operate on a separate thread.
streamingClient.run()
