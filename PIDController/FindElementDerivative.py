def FindElementDerivative(List2D,List2Parameter):
    Array = []
    for i in range(0,len(List2D)-1):
        Array.append(List2D[i][List2Parameter])
    if len(Array)<=1:
        ElementDerivative = 0
    else:
        ElementDerivative = sum(Array[1:len(Array)])/len(Array[1:len(Array)])-sum(Array[:len(Array)-1])/len(Array[:len(Array)-1])
    return ElementDerivative
