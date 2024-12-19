import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
from sklearn.preprocessing import StandardScaler
import pandas as pd
def segment(Filename,prominence, distance, height):
    """
    Segments the accelerometer data into separate shots based on gyro data peaks.

    Parameters:
    bData (str): The path to the CSV file containing the accelerometer data.

    Returns:
    SignalX_Accel (ndarray): Array containing the X-axis acceleration data for each shot.
    SignalY_Accel (ndarray): Array containing the Y-axis acceleration data for each shot.
    SignalZ_Accel (ndarray): Array containing the Z-axis acceleration data for each shot.
    SignalTime (ndarray): Array containing the time domain data for each shot.
    """
    # Function code goes here
#Convert CSV file to pandas then numpy array
    # bData = np.genfromtxt(bData, delimiter=',', skip_header=1)
    file= pd.read_csv(Filename)
    # Backhand data set
    bData = file.to_numpy()
    # scaler = StandardScaler()
    # bData = scaler.fit_transform(bData)
    bPacketNumber = bData[:, 0]
    f= 101 # because the frequency used is 128Hz
    bTimedomain = bPacketNumber / f   # because the frequency used is 128Hz
    bGyroX = bData[:, 1]
    bGyroY = bData[:, 2]
    bGyroZ = bData[:, 3]
    bAccelerationX = bData[:, 4]
    bAccelerationY = bData[:, 5]
    bAccelerationZ = bData[:, 6]

    # Absolute magnitude of gyro data and curve smoothing
    bAccelMean = np.sqrt((bAccelerationX**2) + (bAccelerationY**2) + (bAccelerationZ**2))  # absolute magnitude backhand
    bGyroMean = np.sqrt((bGyroX**2) + (bGyroY**2) + (bGyroZ**2))  # absolute magnitude backhand
    windowSize = 40
    bGyroMeanMovav = np.convolve(bGyroMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
    bpks, _ = find_peaks(bGyroMeanMovav, prominence=prominence, distance=distance, height=height)  # peak distance of 2s and min peak height of .600
    print(len(bpks))
    plt.figure()
    plt.plot(np.arange(0, len(bGyroMeanMovav))/f, bGyroMeanMovav)
    plt.scatter(bpks/f,bGyroMeanMovav[bpks],c="r")
    plt.xlabel('Time (s)')  # x-axis label
    plt.ylabel('Gyro magnitude (�/s)')  # y-axis label
    
    # Saving each shot into separate column of one big array
    # shot length is assumed to be 5s in length
    SignalTime = np.zeros((504, len(bpks)))
    SignalX_Accel = np.zeros((504, len(bpks)))
    SignalY_Accel = np.zeros((504, len(bpks)))
    SignalZ_Accel = np.zeros((504, len(bpks)))
    SignalX_Gyro = np.zeros((504, len(bpks)))
    SignalY_Gyro = np.zeros((504, len(bpks)))
    SignalZ_Gyro = np.zeros((504, len(bpks)))

    for j in range(len(bpks)):
        timeIndex = bpks[j]  # select first time value of peak
        startSignal = timeIndex - 252  # subtract 2.5s worth of data points from peak to obtain time when shot begins
        endSignal = timeIndex + 252  # add 2.5s worth of data points from peak to obtain end of signal
        if j == 0:
            startSignal = 0
            endSignal = 504
        elif j == len(bpks) - 1:
            startSignal = len(bTimedomain) - 504
            endSignal = len(bTimedomain)

        SignalTime[:, j] = bTimedomain[startSignal:endSignal]  # 1 shot in time index to be saved in Signal matrix
        SignalX_Gyro[:, j] = bGyroX[startSignal:endSignal]
        SignalY_Gyro[:, j] = bGyroY[startSignal:endSignal]
        SignalZ_Gyro[:, j] = bGyroZ[startSignal:endSignal]
        SignalX_Accel[:, j] = bAccelerationX[startSignal:endSignal]
        SignalY_Accel[:, j] = bAccelerationY[startSignal:endSignal]
        SignalZ_Accel[:, j] = bAccelerationZ[startSignal:endSignal]

    plt.figure()
    for plotIdx in range(SignalX_Accel.shape[1]):
        plt.plot(SignalX_Accel[:, plotIdx], 'r')  # overlay all forehand shots onto 1 curve
        plt.plot(SignalY_Accel[:, plotIdx], 'g')  # overlay all forehand shots onto 1 curve
        plt.plot(SignalZ_Accel[:, plotIdx], 'b')  # overlay all forehand shots onto 1 curve
        plt.legend(['a_x', 'a_y', 'a_z'])
    plt.xlabel('Time (s)')  # x-axis label
    plt.ylabel('Acceleration (�/s)')  # y-axis label
    plt.legend().set_visible(False)

    # Uncomment the following lines if you want to plot the data
    # plt.figure()
    # for plotIdx in range(SignalX_Accel.shape[1]):
    #     plt.plot(SignalX_Accel[:, plotIdx], 'r')  # overlay all forehand shots onto 1 curve
    #     plt.xlabel('Time (s)')  # x-axis label
    #     plt.ylabel('Acceleration (g)')  # y-axis label
    #     plt.title('X Acceleration in Time Domain')
    # plt.figure()
    # for plotIdx in range(SignalX_Accel.shape[1]):
    #     plt.plot(SignalY_Accel[:, plotIdx], 'g')  # overlay all forehand shots onto 1 curve
    #     plt.xlabel('Time (s)')  # x-axis label
    #     plt.ylabel('Acceleration (g)')  # y-axis label
    #     plt.title('Y Acceleration in Time Domain')
    # plt.figure()
    # for plotIdx in range(SignalX_Accel.shape[1]):
    #     plt.plot(SignalZ_Accel[:, plotIdx], 'b')  # overlay all forehand shots onto 1 curve
    #     plt.xlabel('Time (s)')  # x-axis label

    #     plt.ylabel('Acceleration (g)')  # y-axis label
    #     plt.title('Z Acceleration in Time Domain')

    return SignalX_Gyro,SignalY_Gyro,SignalZ_Gyro,SignalX_Accel, SignalY_Accel, SignalZ_Accel, SignalTime