from FindElementAverage import FindElementAverage
from FindElementDerivative import FindElementDerivative

def FilteredAverage(frames, position, rotation, eulerAngles):
    # frames = [frameNo, systemtime, ischanged], position, rotation, eulerAngles = [theta, phi, psi]
    dt = FindElementDerivative(frames,1)
##    print(dt)
    FilteredPosition = []
    FilteredPosition.append(FindElementAverage(position,0))
    FilteredPosition.append(FindElementAverage(position,1))
    FilteredPosition.append(FindElementAverage(position,2))
    FilteredPositionRate = []
    FilteredPositionRate.append(FindElementDerivative(position,0))
    FilteredPositionRate.append(FindElementDerivative(position,1))
    FilteredPositionRate.append(FindElementDerivative(position,2))
    FilteredRotation = []
    FilteredRotation.append(FindElementAverage(rotation,0))
    FilteredRotation.append(FindElementAverage(rotation,1))
    FilteredRotation.append(FindElementAverage(rotation,2))
    FilteredRotation.append(FindElementAverage(rotation,3))
    FilteredRotationRate = []
    FilteredRotationRate.append(FindElementDerivative(rotation,0))
    FilteredRotationRate.append(FindElementDerivative(rotation,1))
    FilteredRotationRate.append(FindElementDerivative(rotation,2))
    FilteredRotationRate.append(FindElementDerivative(rotation,3))
    FilteredEuler = []
    FilteredEuler.append(FindElementAverage(eulerAngles,0))
    FilteredEuler.append(FindElementAverage(eulerAngles,1))
    FilteredEuler.append(FindElementAverage(eulerAngles,2))
    FilteredEulerRate = []
    FilteredEulerRate.append(FindElementDerivative(eulerAngles,0))
    FilteredEulerRate.append(FindElementDerivative(eulerAngles,1))
    FilteredEulerRate.append(FindElementDerivative(eulerAngles,2))

    return dt,FilteredPosition,FilteredPositionRate,FilteredRotation,FilteredRotationRate,FilteredEuler,FilteredEulerRate
