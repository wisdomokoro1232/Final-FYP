from segment_Accel import segment
import numpy as np
def Compile_Volley(filenames):
    n= len(filenames)
    for i in range(n):
        if i == 0:
            AllfGyroX, AllfGyroY, AllfGyroZ,AllfAccelX, AllfAccelY, AllfAccelZ, AllfAccelTime = segment(filenames[i])
        else:
            DfGyroX, DfGyroY, DfGyroZ,DfAccelX, DfAccelY, DfAccelZ, DfGyroTime = segment(filenames[i])
            AllfGyroX = np.hstack((AllfGyroX, DfGyroX))
            AllfGyroY = np.hstack((AllfGyroY, DfGyroY))
            AllfGyroZ = np.hstack((AllfGyroZ, DfGyroZ))
            AllfAccelX = np.hstack((AllfAccelX, DfAccelX))
            AllfAccelY = np.hstack((AllfAccelY, DfAccelY))
            AllfAccelZ = np.hstack((AllfAccelZ, DfAccelZ))

    return AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ