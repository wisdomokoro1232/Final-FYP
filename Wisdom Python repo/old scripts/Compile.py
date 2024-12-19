from segment_Gyro import segment
import numpy as np
def Compile(filenames,distance=252,height=200,prominence=100):
    n= len(filenames)
    for i in range(0,n):
        if i == 0:
            AllfGyroX, AllfGyroY, AllfGyroZ,AllfAccelX, AllfAccelY, AllfAccelZ, AllfAccelTime = segment(filenames[i],prominence,distance,height)
        else:
            DfGyroX, DfGyroY, DfGyroZ,DfAccelX, DfAccelY, DfAccelZ, DfGyroTime = segment(filenames[i],prominence,distance,height)
            AllfGyroX = np.hstack((AllfGyroX, DfGyroX))
            AllfGyroY = np.hstack((AllfGyroY, DfGyroY))
            AllfGyroZ = np.hstack((AllfGyroZ, DfGyroZ))
            AllfAccelX = np.hstack((AllfAccelX, DfAccelX))
            AllfAccelY = np.hstack((AllfAccelY, DfAccelY))
            AllfAccelZ = np.hstack((AllfAccelZ, DfAccelZ))

    return AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ