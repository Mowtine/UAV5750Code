import numpy

def FindElementAverage(List2D,List2Parameter):
##    print(List2D)
##    print(List2Parameter)
    Array = []
    for i in range(0,len(List2D)-1):
        Array.append(List2D[i][List2Parameter])
    if len(Array)<=0:
        ElementAverage =0
    else:
        ElementAverage = sum(Array)/len(Array)
    return ElementAverage

def FindAngleAverage(List2D,List2Parameter):
##    print(List2D)
##    print(List2Parameter)
    Array = []
    for i in range(0,len(List2D)-1):
        Array.append(List2D[i][List2Parameter])
    Array = numpy.unwrap(Array)
    if len(Array)<=0:
        ElementAverage =0
    else:
        ElementAverage = sum(Array)/len(Array)
    return ElementAverage
