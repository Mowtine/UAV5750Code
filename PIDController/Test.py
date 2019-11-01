import PID as PIDFile

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

print(vbarVal)


valuesrc = [0,0,0,0,0,0,0]
frames   = [[0,1,0],[0,0,1],[0,0,1]]
position = [[0,0,5],[2,0,0],[2,0,0]]
rotation = [[0,5,0,0],[1,0,0,0],[1,0,0,0]]
eulerAngles = [[1,0,0],[0,2,0],[0,0,0]]

PID = PIDFile.PID(valuesrc,frames,position,rotation,eulerAngles, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.3, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
vbarVal = PID.run(valuesrc,frames,position,rotation,eulerAngles);

print(vbarVal)
