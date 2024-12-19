import numpy as np

def MaxMin(fGyroX, fGyroY, fGyroZ, fAccelX, fAccelY, fAccelZ):
    # Minimum
    gMin = np.array([np.min(fGyroX, axis=0), np.min(fGyroY, axis=0), np.min(fGyroZ, axis=0)]).T
    aMin = np.array([np.min(fAccelX, axis=0), np.min(fAccelY, axis=0), np.min(fAccelZ, axis=0)]).T

    # Maximum
    gMax = np.array([np.max(fGyroX, axis=0), np.max(fGyroY, axis=0), np.max(fGyroZ, axis=0)]).T
    aMax = np.array([np.max(fAccelX, axis=0), np.max(fAccelY, axis=0), np.max(fAccelZ, axis=0)]).T

    # Mean
    gMean = np.array([np.mean(fGyroX, axis=0), np.mean(fGyroY, axis=0), np.mean(fGyroZ, axis=0)]).T
    aMean = np.array([np.mean(fAccelX, axis=0), np.mean(fAccelY, axis=0), np.mean(fAccelZ, axis=0)]).T

    # Std
    gStd = np.array([np.std(fGyroX, axis=0), np.std(fGyroY, axis=0), np.std(fGyroZ, axis=0)]).T
    aStd = np.array([np.std(fAccelX, axis=0), np.std(fAccelY, axis=0), np.std(fAccelZ, axis=0)]).T

    # Under curve
    gArea = np.array([np.trapz(fGyroX, axis=0), np.trapz(fGyroY, axis=0), np.trapz(fGyroZ, axis=0)]).T
    aArea = np.array([np.trapz(fAccelX, axis=0), np.trapz(fAccelY, axis=0), np.trapz(fAccelZ, axis=0)]).T

    return aMax, aMin, aMean, aStd, aArea, gMax, gMin, gMean, gStd, gArea