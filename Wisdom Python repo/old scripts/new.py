#%%
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import joblib
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
import pandas as pd
from scipy import signal
from scipy.ndimage import shift
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import ensemble
from functools import reduce
import os
import coremltools
import itertools
from scipy import stats
#regex module
import re
from scipy.spatial import distance
pattern = r'[0-9]'
#%%
"""
This script loads an svm model and converts it to a coreml model for use in apple devices
"""
# path_windows= '/Users/wwo20/OneDrive - Imperial College London/'
# path_mac= '/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/'
# path= path_windows
# full_path= f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/'
# #load scaler parameters
# scaler_PARAMS= pd.read_csv(f'{full_path}my data/scaling_params.csv')
# scaler= StandardScaler()
# scaler.mean_= scaler_PARAMS['mean']
# scaler.scale_= scaler_PARAMS['scale']

# #load svm model
# svmodel= joblib.load(f'{full_path}MODELS/Main_svm_5class99PCA%.pkl')
# #load pca model
# pca= joblib.load(f'{full_path}MODELS/pca99_5shot.pkl')
# pipe= Pipeline(steps=[('scaler',scaler),('pca',pca),('svm',svmodel)])
# #convert to coreml
# print('Converting to CoreML')
# coreml_model = convert(svmodel)
# coreml_model.save(f'{full_path}SVM_5_Class.mlmodel')
#%%
def Compile(filenames,distance=200,height=5.5,prominence=1,plot=False,shot_length=2.5):
    n= len(filenames)
    for i in range(0,n):
        if i == 0: #AllfPitch, AllfRoll,AllfYaw   DfPitch, DfRoll,DfYaw
            AllfGyroX, AllfGyroY, AllfGyroZ,AllfAccelX, AllfAccelY, AllfAccelZ, AllfAccelTime,AllfPitch, AllfRoll,AllfYaw,Allname,Allshot,Allshots_made   = segment(filenames[i],prominence,distance,height,100,shot_length,plot)
        else:
            DfGyroX, DfGyroY, DfGyroZ,DfAccelX, DfAccelY, DfAccelZ,DfGyroTime,DfPitch, DfRoll,DfYaw,Dname,Dshot,Dshots_made = segment(filenames[i],prominence,distance,height,100,shot_length,plot)
            AllfGyroX = np.hstack((AllfGyroX, DfGyroX))
            AllfGyroY = np.hstack((AllfGyroY, DfGyroY))
            AllfGyroZ = np.hstack((AllfGyroZ, DfGyroZ))
            AllfAccelX = np.hstack((AllfAccelX, DfAccelX))
            AllfAccelY = np.hstack((AllfAccelY, DfAccelY))
            AllfAccelZ = np.hstack((AllfAccelZ, DfAccelZ))
            AllfPitch = np.hstack((AllfPitch, DfPitch))
            AllfRoll = np.hstack((AllfRoll, DfRoll))
            AllfYaw = np.hstack((AllfYaw, DfYaw))
            Allname= np.hstack((Allname, Dname))
            Allshot= np.hstack((Allshot, Dshot))
            Allshots_made= np.hstack((Allshots_made, Dshots_made))

    return AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ,AllfPitch, AllfRoll,AllfYaw,Allname,Allshot,Allshots_made

# Compiling dishas shots- different parameters for segmentation and detection
def Compile_disha(filenames,distance=256,height=300,prominence=200,plot=True):
    n= len(filenames)
    for i in range(0,n):
        if i == 0:
            AllfGyroX, AllfGyroY, AllfGyroZ,AllfAccelX, AllfAccelY, AllfAccelZ, AllfAccelTime = segment(filenames[i],prominence,distance,height,128,plot=True)
        else:
            DfGyroX, DfGyroY, DfGyroZ,DfAccelX, DfAccelY, DfAccelZ, DfGyroTime = segment(filenames[i],prominence,distance,height,128,plot=True)
            AllfGyroX = np.hstack((AllfGyroX, DfGyroX))
            AllfGyroY = np.hstack((AllfGyroY, DfGyroY))
            AllfGyroZ = np.hstack((AllfGyroZ, DfGyroZ))
            AllfAccelX = np.hstack((AllfAccelX, DfAccelX))
            AllfAccelY = np.hstack((AllfAccelY, DfAccelY))
            AllfAccelZ = np.hstack((AllfAccelZ, DfAccelZ))

    return AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ

def segment_disha(Filename,prominence, distance, height,frequency,plot=False):
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
    global file
    file= pd.read_csv(Filename)
    # Backhand data set
    bData = file.to_numpy()
    # scaler = StandardScaler()
    # bData = scaler.fit_transform(bData)
    bPacketNumber = np.arange(0,len(bData[:, 0]))
    f= frequency # because the frequency used is 128Hz
    bTimedomain = bPacketNumber / f   # because the frequency used is 128Hz
   
    if plot:
        plt.figure()
    if "nertial" in Filename:
        bGyroX = bData[:, 1]
        bGyroY = bData[:, 2]
        bGyroZ = bData[:, 3]
        bAccelerationX = bData[:, 4]
        bAccelerationY = bData[:, 5]
        bAccelerationZ = bData[:, 6]
        windowSize = 40
        # bAccelMean = np.sqrt((bAccelerationX**2) + (bAccelerationY**2) + (bAccelerationZ**2))  # absolute magnitude accel
        # bMeanMovav = np.convolve(bAccelMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
        bGyroMean = np.sqrt((bGyroX**2) + (bGyroY**2) + (bGyroZ**2))  # absolute magnitude gyro
        bMeanMovav = np.convolve(bGyroMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
        print('disha')
        if plot:
            plt.ylabel('Gyro magnitude (deg/s)')
    else:
        windowSize = 5
        bGyroX = bData[:, 4]
        bGyroY = bData[:, 5]
        bGyroZ = bData[:, 6]
        bAccelerationX = bData[:, 1]
        bAccelerationY = bData[:, 2]
        bAccelerationZ = bData[:, 3]
        bGyroMean = np.sqrt((bGyroX**2) + (bGyroY**2) + (bGyroZ**2))  # absolute magnitude gyro
        bMeanMovav = np.convolve(bGyroMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
        if plot:
            plt.ylabel('Gyro magnitude (�/s)')
    print(f'{Filename}')
    bpks, _ = find_peaks(bMeanMovav, prominence=prominence, distance=distance, height=height)  # peak distance of 2s and min peak height of .600
    if plot:
        plt.plot(np.arange(0, len(bMeanMovav))/f, bMeanMovav)
        plt.scatter(bpks/f,bMeanMovav[bpks],c="r")
        plt.xlabel('Time (s)')  # x-axis label
      # y-axis label
    shot_len = 2.5 # seconds
  
    size = int(shot_len*f)
    # Saving each shot into separate column of one big array
    # shot length is assumed to be 5s in length
    SignalTime = np.zeros((size, len(bpks)))
    SignalX_Accel = np.zeros((size, len(bpks)))
    SignalY_Accel = np.zeros((size, len(bpks)))
    SignalZ_Accel = np.zeros((size, len(bpks)))
    SignalX_Gyro = np.zeros((size, len(bpks)))
    SignalY_Gyro = np.zeros((size, len(bpks)))
    SignalZ_Gyro = np.zeros((size, len(bpks)))
    print(SignalTime.shape)
    half_shot= int(size/2)
    for j in range(len(bpks)):
        timeIndex = bpks[j]  # select first time value of peak
        if j == 0:
            startSignal = 0
            endSignal = size
        elif j == len(bpks) - 1:
            startSignal = len(bTimedomain) - size
            endSignal = len(bTimedomain)
        else:
            startSignal = timeIndex - half_shot# subtract 2.5s worth of data points from peak to obtain time when shot begins
            endSignal = timeIndex + half_shot# add 2.5s worth of data points from peak to obtain end of signal
        SignalTime[:, j] = bTimedomain[startSignal:endSignal]  # 1 shot in time index to be saved in Signal matrix
        SignalX_Gyro[:, j] = bGyroX[startSignal:endSignal]
        SignalY_Gyro[:, j] = bGyroY[startSignal:endSignal]
        SignalZ_Gyro[:, j] = bGyroZ[startSignal:endSignal]
        SignalX_Accel[:, j] = bAccelerationX[startSignal:endSignal]
        SignalY_Accel[:, j] = bAccelerationY[startSignal:endSignal]
        SignalZ_Accel[:, j] = bAccelerationZ[startSignal:endSignal]

    #normalise the yaw pitch and roll values v=
    # plt.figure()
    # fig, axs = plt.subplots()
    # fig2, axs2 = plt.subplots()
    # fig3, axs3 = plt.subplots()
    # axs.title.set_text('a_x')
    # axs2.title.set_text('a_y')
    # axs3.title.set_text('a_z')
    # for plotIdx in range(SignalX_Accel.shape[1]):
    #     axs.plot(SignalX_Accel[:, plotIdx], 'r')  # overlay all forehand shots onto 1 curve
    #     axs2.plot(SignalY_Accel[:, plotIdx], 'g')  # overlay all forehand shots onto 1 curve
    #     axs3.plot(SignalZ_Accel[:, plotIdx], 'b')  # overlay all forehand shots onto 1 curve
    # plt.xlabel('Time (s)')  # x-axis label
    # plt.ylabel('Acceleration (�/s)')  # y-axis label


    #Uncomment the following lines if you want to plot the data
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
    # plt.show()
    # plt.close()
    return SignalX_Gyro,SignalY_Gyro,SignalZ_Gyro,SignalX_Accel, SignalY_Accel, SignalZ_Accel, SignalTime

def segment(Filename,prominence, distance, height,frequency,shot_length,plot=False):
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
    global pattern
    file= pd.read_csv(Filename)
    # Backhand data set
    bData = file.to_numpy()
    # scaler = StandardScaler()
    # bData = scaler.fit_transform(bData)
    bPacketNumber = np.arange(0,len(bData[:, 0]))
    f= frequency # because the frequency used is 128Hz
    bTimedomain = bPacketNumber / f   # because the frequency used is 128Hz
    shot= Filename.split('Watch Sensor/')[1].split('_')[0]
    shots_made=  Filename.split('Watch Sensor')[1].split('/Motion')[0].split(shot+'_')[1].split('_')[0]
    name= Filename.split('Watch Sensor')[1].split('/Motion')[0].split(shot+'_')[1].split('_')[1]
    #some motion csv were named like shottype_shotsmade_name2.. name3, if it was the same multiple of shot for the same shot type
    #So take awya the numbers
    name= re.sub(pattern, '', name)
    windowSize = 10
    bGyroX = bData[:, 4]
    bGyroY = bData[:, 5]
    bGyroZ = bData[:, 6]
    bAccelerationX = bData[:, 1]
    bAccelerationY = bData[:, 2]
    bAccelerationZ = bData[:, 3]
    bAccelMean = np.sqrt((bAccelerationX**2) + (bAccelerationY**2) + (bAccelerationZ**2))  # absolute magnitude accel
    bAccelMeanMovav = np.convolve(bAccelMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
    bGyroMean = np.sqrt((bGyroX**2) + (bGyroY**2) + (bGyroZ**2))  # absolute magnitude gyro
    bMeanMovav = np.convolve(bGyroMean, np.ones(windowSize), 'valid') / windowSize  # moving average backhand
    bPitch= bData[:, 10]
    bRoll= bData[:, 11]
    bYaw= bData[:, 12]
    print(f'{Filename}')
    bpks, _ = find_peaks(bMeanMovav, prominence=prominence, distance=distance, height=height)  # peak distance of 2s and min peak height of .600
    #check if acceleration magnitude is above 2, from data this should be true for even the weakest shots. It seperates non shot actions
    bpks= bpks[bAccelMeanMovav[bpks]>1]
    if plot:
        plt.figure()
        plt.ylabel('Gyro magnitude (�/s)')
        plt.plot(np.arange(0, len(bMeanMovav))/f, bMeanMovav)
        plt.scatter(bpks/f,bMeanMovav[bpks],c="r")
        plt.xlabel('Time (s)')  # x-axis label
      # y-axis label
    shot_len = shot_length # seconds
  
    size = int(shot_len*f)
    # Saving each shot into separate column of one big array
    # shot length is assumed to be 5s in length
    SignalTime = np.zeros((size, len(bpks)))
    SignalX_Accel = np.zeros((size, len(bpks)))
    SignalY_Accel = np.zeros((size, len(bpks)))
    SignalZ_Accel = np.zeros((size, len(bpks)))
    SignalX_Gyro = np.zeros((size, len(bpks)))
    SignalY_Gyro = np.zeros((size, len(bpks)))
    SignalZ_Gyro = np.zeros((size, len(bpks)))
    Signal_pitch= np.zeros((size, len(bpks)))
    Signal_roll= np.zeros((size, len(bpks)))
    Signal_yaw= np.zeros((size, len(bpks)))
    print(SignalTime.shape)
    half_shot= int(size/2)
    for j in range(len(bpks)):
        timeIndex = bpks[j]  # select first time value of peak
        if j == 0:
            startSignal = 0
            endSignal = size
        elif j == len(bpks) - 1:
            startSignal = len(bTimedomain) - size
            endSignal = len(bTimedomain)
        else:
            startSignal = timeIndex - half_shot# subtract 2.5s worth of data points from peak to obtain time when shot begins
            endSignal = timeIndex + half_shot# add 2.5s worth of data points from peak to obtain end of signal
        SignalTime[:, j] = bTimedomain[startSignal:endSignal]  # 1 shot in time index to be saved in Signal matrix
        SignalX_Gyro[:, j] = bGyroX[startSignal:endSignal]
        SignalY_Gyro[:, j] = bGyroY[startSignal:endSignal]
        SignalZ_Gyro[:, j] = bGyroZ[startSignal:endSignal]
        SignalX_Accel[:, j] = bAccelerationX[startSignal:endSignal]
        SignalY_Accel[:, j] = bAccelerationY[startSignal:endSignal]
        SignalZ_Accel[:, j] = bAccelerationZ[startSignal:endSignal]
        Signal_pitch[:, j] = bPitch[startSignal:endSignal]
        Signal_roll[:, j] = bRoll[startSignal:endSignal]
        Signal_yaw[:, j] = bYaw[startSignal:endSignal]
        #normalise the yaw pitch and roll values by their starting value since we dont care about teh absolute
        #only the change in rotation
        Signal_pitch[:, j] = Signal_pitch[:, j] - Signal_pitch[0, j]
        Signal_roll[:, j] = Signal_roll[:, j] - Signal_roll[0, j]
        Signal_yaw[:, j] = Signal_yaw[:, j] - Signal_yaw[0, j]
    
    #convert to degrees
    Signal_pitch= np.degrees(Signal_pitch)
    Signal_roll= np.degrees(Signal_roll)
    Signal_yaw= np.degrees(Signal_yaw)

    # plt.figure()
    # fig, axs = plt.subplots()
    # fig2, axs2 = plt.subplots()
    # fig3, axs3 = plt.subplots()
    # axs.title.set_text('a_x')
    # axs2.title.set_text('a_y')
    # axs3.title.set_text('a_z')
    # for plotIdx in range(SignalX_Accel.shape[1]):
    #     axs.plot(SignalX_Accel[:, plotIdx], 'r')  # overlay all forehand shots onto 1 curve
    #     axs2.plot(SignalY_Accel[:, plotIdx], 'g')  # overlay all forehand shots onto 1 curve
    #     axs3.plot(SignalZ_Accel[:, plotIdx], 'b')  # overlay all forehand shots onto 1 curve
    # plt.xlabel('Time (s)')  # x-axis label
    # plt.ylabel('Acceleration (�/s)')  # y-axis label


    #Uncomment the following lines if you want to plot the data
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
    # plt.show()
    return SignalX_Gyro,SignalY_Gyro,SignalZ_Gyro,SignalX_Accel, SignalY_Accel, SignalZ_Accel, SignalTime ,Signal_pitch,Signal_roll,Signal_yaw,[name]*len(bpks),shot,int(shots_made)

def feature_template(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ,title, AllSignal_pitch, AllSignal_roll,AllSignal_yaw,shot,shot_template):
    # Angular Velocities
    AllfGyro_av = np.mean(np.array([AllfGyroX, AllfGyroY, AllfGyroZ]), axis=0)
    num_shots= AllfGyroX.shape[1]
    # Racket linear speed
    R = 0.7445  # radius from shoulder to point of impact of ball
    Maxes = np.max(np.abs(AllfGyro_av), axis=0)
    Peaky = Maxes[1]
    Peakz = Maxes[2]
    omega = np.sqrt((Peaky * 0.0174533) ** 2 + (Peakz * 0.0174533) ** 2)
    LinSpeed = omega * R

    # Spin Rating
    maxiY = np.max(np.abs(AllfGyroY))
    maxY = np.max(maxiY)
    minY = np.min(maxiY)
    maxiZ = np.max(np.abs(AllfGyroZ))
    maxZ = np.max(maxiZ)
    minZ = np.min(maxiZ)
    if maxiY.size > 0 and maxiZ.size > 0:
        omega_high = np.sqrt(maxY ** 2 + maxZ ** 2)
        omega_low = np.sqrt(minY ** 2 + minZ ** 2)
        theta_high = omega_high * 0.12
        theta_low = omega_low * 0.12
    else:
        theta_high = 0
        theta_low = 0
    #Calculater euclidean distance for shots
    std_scale= StandardScaler()
    global Accel_template
    Accel_template = shot_template[:, :3]
    Gyro_template = shot_template[:, 3:]
   
    # Accel_template = std_scale.fit_transform(Accel_template)
    # Gyro_template = std_scale.fit_transform(Gyro_template)
    global player_Accel
    player_Accel = np.array([AllfAccelX, AllfAccelY, AllfAccelZ])
    player_Gyro = np.array([AllfGyroX,AllfGyroY, AllfGyroZ])
    player_Accel = np.transpose(player_Accel, (1, 0, 2))
    player_Gyro = np.transpose(player_Gyro, (1, 0, 2))
    # calculate distance for each axis
    global distance_Accel
    distance_Accel= np.zeros((player_Accel.shape[1], num_shots))
    distance_Gyro= np.zeros((player_Gyro.shape[1], num_shots))
    for i in range(num_shots):
        for j in range(3):
            distance_Accel[j,i] = distance.euclidean(player_Accel[:,j,i], Accel_template[:,j])
            distance_Gyro[j,i] = distance.euclidean(player_Gyro[:,j,i], Gyro_template[:,j])
    # plot the different euclidean distances for each player
    global players
    fig1, ax1 = plt.subplots(1, 1)
    fig2, ax2 = plt.subplots(1, 1)
    fig_avgacc, ax_avgaccel = plt.subplots(1, 1)
    fig_avggyr, ax_gyro = plt.subplots(1, 1)
    fig1.suptitle(f'Euclidean distance for {np.unique(shot)}')
    fig2.suptitle(f'Euclidean distance for {np.unique(shot)}')
    fig_avgacc.suptitle(f'Average Euclidean distance for {np.unique(shot)}')
    fig_avggyr.suptitle(f'Average Euclidean distance for {np.unique(shot)}')
    ax1.set_title('Acceleration')
    ax2.set_title('Gyroscope')
    ax_avgaccel.set_title('Acceleration')
    ax_gyro.set_title('Gyroscope')
    colors = itertools.cycle(["r", "b", "g"])
    color_dict = {}  # Initialize the color dictionary
    for player in players:
        global distance_Accel_player
        distance_Accel_player = distance_Accel[:,title==player]
        distance_Gyro_player = distance_Gyro[:,title==player]
        if distance_Accel_player.size > 0 and distance_Gyro_player.size > 0:
            for i in range(3):
                x_values = [player] * distance_Accel_player.shape[1]
                col = color_dict.get(i, next(colors))  # Get the color for the player from the dictionary or assign a new color
                color_dict[i] = col  # Store the color for the player in the dictionary
                label = f'{chr(120+i)}'
                accelavg= stats.trim_mean(distance_Accel_player[i, :],0.1)
                gyroavg= stats.trim_mean(distance_Gyro_player[i, :],0.1)
                marker_size = 5  # Adjust the marker size as desired
                ax_avgaccel.scatter(player, accelavg, c=col, label=label, s=marker_size)
                ax_gyro.scatter(player, gyroavg, c=col, label=label, s=marker_size)
                ax1.scatter(x_values, distance_Accel_player[i, :], c=col, label=label, s=marker_size)
                ax2.scatter(x_values, distance_Gyro_player[i, :], c=col, label=label, s=marker_size)
            # avg_gyro_distance = np.mean(distance_Gyro_player, axis=0)
            # avg_accel_distance = np.mean(distance_Accel_player, axis=0)
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
   
    handles, labels = ax2.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax2.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    handles, labels = ax_avgaccel.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax_avgaccel.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    handles, labels = ax_gyro.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax_gyro.legend(by_label.values(), by_label.keys(),bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    ax1.set_xlabel('Player')
    ax1.set_ylabel('Euclidean Distance')
    ax2.set_xlabel('Player')
    ax2.set_ylabel('Euclidean Distance')
    plt.show()
    #Now plot the averafe distance for each player
    # global distance_Accel_av
    # distance_Accel_av = np.mean(distance_Accel, axis=0)
    # distance_Gyro_av = np.mean(distance_Gyro, axis=0)
    # Plotting
    # plt.figure()
    # plt.plot(AllfGyro_av[0, :], 'r', linewidth=1.5)
    # plt.plot(AllfGyro_av[1, :], 'g', linewidth=1.5)
    # plt.plot(AllfGyro_av[2, :], 'b', linewidth=1.5)
    # plt.legend(['\omega_x', '\omega_y', '\omega_z'])
    # plt.xlabel('Time (s)')  # x-axis label
    # plt.ylabel('Gyroscope (°/s)')  # y-axis label

    # Acceleration mag for Power Rating
    AllfAccel_av = np.mean(np.array([AllfAccelX, AllfAccelY, AllfAccelZ]), axis=0)
    MagAccel = np.sqrt(AllfAccelZ ** 2)  # magnitude of acceleration for all shots
    MagAccelPeaks = MagAccel[229:237, :]
    MagAccelmeans = np.mean(MagAccelPeaks, axis=0)
    if MagAccelmeans.size > 0:
        magA_low = np.min(MagAccelmeans[:], axis=0)
        magA_high = np.max(MagAccelmeans[:])
    else:
        magA_low = 0
        magA_high = 0
 
     
    # global eval('title[]')
    #unique values in title
    # global players
    # for i in players:
    #     Signal_pitch= AllSignal_pitch[:,title==i]
    #     if Signal_pitch.size > 0:
    #         fig2,ax2= plt.subplots(1,1)
    #         fig2.suptitle(f'Average {np.unique(shot)[0]} Rotations for '+ i)
    #         Signal_roll= AllSignal_roll[:,title==i]
    #         Signal_yaw= AllSignal_yaw[:,title==i]
    #         rotation_average= np.array([[np.average(Signal_pitch,axis=1)], [np.average(Signal_roll,axis=1)], [np.average(Signal_yaw,axis=1)]])
    #         pitch_smoothness= np.std(np.diff(Signal_pitch)).round(2)
    #         # roll_smoothness= np.std(np.diff(Signal_roll)).round(2)
            # yaw_smoothness= np.std(np.diff(Signal_yaw)).round(2)
            # for j in range(rotation_average.shape[0]):
            #     ax2.plot(rotation_average[j,0,:]) 
            #     ax2.set_xlabel('Time (s)')
            #     ax2.set_ylabel('Rotation (�/s)')
            # plt.legend([f'Pitch with smoothness {pitch_smoothness}', f'Roll with smoothness {roll_smoothness}', f'Yaw with smoothness {yaw_smoothness}'], loc='lower left')
            # plt.show()
            # Accelx= AllfAccelX[:,title==i]
            # Accely= AllfAccelY[:,title==i]
            # Accelz= AllfAccelZ[:,title==i]
            # print(Accelx.shape)
            # Accel=['x','y','z']
            # fig,ax= plt.subplots(3,1,sharex=True)
            # fig.suptitle(f'Average {np.unique(shot)[0]} Acceleration for '+ i)
            # ax[2].set_xlabel('Time (s)')
            # for j in range(3):
            #     ax[j].plot(np.average(eval(f'Accel{Accel[j]}'),axis=1))
            #     ax[j].set_ylabel('Acceleration (g) in ' + Accel[j])
            # plt.show()
    return AllfGyro_av, AllfAccel_av, LinSpeed, theta_high, theta_low, magA_low, magA_high

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

def Cross_cor_template(SignalXG, SignalYG, SignalZG,SignalXA, SignalYA, SignalZA,freq, avgtemplate,length=2.5):
    # From analyssi we know that the templates of YA XG AND ZG are most consistent, so we will use them to align the data
    size= int(length*freq) # length s of data
    SignalGraph = np.linspace(0,size,size) # Shot in time index (starting at 0) to be used for plotting
    num= len(SignalXG[0,:] )# Number of shots
    print("pre alignment")    # Used for graph for progress report - can be otherwise commented out
    # plt.figure()
     # # Plotting for each signal axis
    # for axis in ['X', 'Y', 'Z']:
    #     plt.figure()
    #     plt.title(f'Gyro {axis} Pre-Alignment')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}G[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Gyro {axis}'], loc='upper right')
    #         else:
    #             pass

    #     plt.figure()
    #     plt.title(f'Accel {axis} Pre-Alignment')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}A[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Accel {axis}'], loc='upper right')
    #         else:
                # pass

    # for each
    global lag_values
    lag_values = np.zeros([num,6])
    for i in range(0,num,1):
        lag_values[i,0]=  np.argmax(signal.correlate(SignalXG[:,i], avgtemplate[:,0]))
        lag_values[i,1]=  np.argmax(signal.correlate(SignalYG[:,i], avgtemplate[:,1]))
        lag_values[i,2]=  np.argmax(signal.correlate(SignalZG[:,i], avgtemplate[:,2]))
        lag_values[i,3]=  np.argmax(signal.correlate(SignalXA[:,i], avgtemplate[:,3]))
        lag_values[i,4]=  np.argmax(signal.correlate(SignalYA[:,i], avgtemplate[:,4]))
        lag_values[i,5]=  np.argmax(signal.correlate(SignalZA[:,i], avgtemplate[:,5]))    
def Display_Signal(SignalXG, SignalYG, SignalZG,SignalXA, SignalYA, SignalZA,freq,title, Signal_pitch, Signal_roll,Signal_yaw,length=2.5):
    # size= int(length*freq) # 2.5s of data
    # SignalGraph = np.linspace(0,size,size)
    # num= len(SignalXG[0,:] )
    # for axis in ['X', 'Y', 'Z']:
    #     plt.figure()
    #     plt.title(f'Gyro {axis} for {title}')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}G[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Gyro {axis}'], loc='upper right')
    #         else:
    #             pass

    #     plt.figure()
    #     plt.title(f'Accel {axis} for {title}')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}A[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Accel {axis}'], loc='upper right')
    #         else:
    #             pass
    # global signal_avg
    # signal_avg= np.array([[np.average(SignalXG,axis=1)], [np.average(SignalYG,axis=1)], [np.average(SignalZG,axis=1)],[np.average(SignalXA,axis=1)], [np.average(SignalYA,axis=1)], [np.average(SignalZA,axis=1)]])
    # # print(template.shape)
    
    # plt.figure()
    # # Plotting 'model' template for the particular class - both methods
    # for i in range(6):
    #     plt.plot(range(size),signal_avg[i,0,:]) 
    # plt.title(f'Average Signal for {title}')
    # plt.legend(['Gyro X', 'Gyro Y', 'Gyro Z', 'Acc. X', 'Acc. Y', 'Acc. Z'])
    # plt.xlabel('Sample No.')
    # plt.ylabel('Value')
    # plt.show()

    # fig,ax= plt.subplots(3,1)
    # fig.suptitle(title)
    # for plotIdx in range(Signal_pitch.shape[1]):
    #     ax[0].plot(Signal_pitch[:, plotIdx], 'r')
    #     ax[0].set_xlabel('Time (s)')  # x-axis label
    #     ax[0].set_ylabel('Pitch (�/s)')  # y-axis label
    # for plotIdx in range(Signal_roll.shape[1]):
    #     ax[1].plot(Signal_roll[:, plotIdx], 'g')
    #     ax[1].set_xlabel('Time (s)')
    #     ax[1].set_ylabel('Roll (�/s)')
    # for plotIdx in range(Signal_yaw.shape[1]):
    #     ax[2].plot(Signal_yaw[:, plotIdx], 'b')
    #     ax[2].set_xlabel('Time (s)')
    #     ax[2].set_ylabel('Yaw (�/s)')
    rotation_average= np.array([[np.average(Signal_pitch,axis=1)], [np.average(Signal_roll,axis=1)], [np.average(Signal_yaw,axis=1)]])
    pitch_smoothness= np.std(np.diff(Signal_pitch)).round(2)
    roll_smoothness= np.std(np.diff(Signal_roll)).round(2)
    yaw_smoothness= np.std(np.diff(Signal_yaw)).round(2)
    fig2,ax2= plt.subplots(1,1)
    fig2.suptitle('Average Rotations'+ title)
    for i in range(rotation_average.shape[0]):
        ax2.plot(rotation_average[i,0,:]) 
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Rotation (�/s)')
    plt.legend([f'Pitch with smoothness {pitch_smoothness}', f'Roll with smoothness {roll_smoothness}', f'Yaw with smoothness {yaw_smoothness}'], loc='lower left')
    plt.show()
    #calculate the smoothness of teh curve by measuring standard deviation of the differences
    #this should indicate how much the curve changes from one point to the next and how this change is distributed
    #also normalise to absolute meanvalue to get a sense of how much the curve changes relative to its mean
    # pitch_smoothness= np.std(np.diff(Signal_pitch))/np.mean(np.abs(Signal_pitch))
    # roll_smoothness= np.std(np.diff(Signal_roll))/np.mean(np.abs(Signal_roll))
    # yaw_smoothness= np.std(np.diff(Signal_yaw))/np.mean(np.abs(Signal_roll))
    # plt.subplot(3,1,1)
    # lag= 3
    # plt.suptitle(f'Autocorrelation with lag= {lag} for ' + title)
    # pd.plotting.lag_plot(rotationdf['Pitch'], lag=lag)
    # plt.title('Pitch with smoothness= '+ str(pitch_smoothness))
    # plt.subplot(3,1,2)
    # plt.title('Roll with smoothness = '+ str(roll_smoothness))
    # pd.plotting.lag_plot(rotationdf['Roll'], lag=lag)
    # plt.subplot(3,1,3)
    # plt.title('Yaw with smoothness = '+ str(yaw_smoothness))
    # pd.plotting.lag_plot(rotationdf['Yaw'], lag=lag)
    # plt.show()
    
def confusion_and_accuracy(y_test, y_pred, labels,title):
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    #
    # Generate confusion matrix
    confusion_mat = confusion_matrix(y_test, y_pred)

    # Create a heatmap of the confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_mat, annot=True, cmap='Blues', fmt='d', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    #
    # Calculate percentages for each class
    confusion_mat_percent = confusion_mat / confusion_mat.sum(axis=1)[:, np.newaxis]

    # Create a heatmap of the confusion matrix with percentages
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_mat_percent, annot=True, cmap='Blues', fmt='.2%', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix (Percentages)')

    plt.show()
    print("Accuracy is", accuracy*100, "%")
def cross_corr(SignalXG, SignalYG, SignalZG,SignalXA, SignalYA, SignalZA,freq=100):
    
    size= int(2.5*freq) # 2.5s of data
    SignalGraph = np.linspace(0,size,size) # Shot in time index (starting at 0) to be used for plotting
    num= len(SignalXG[0,:] )# Number of shots
    print("pre alignment")    # Used for graph for progress report - can be otherwise commented out
    # plt.figure()
    global Signal_prealignment
    Signal_prealignment= np.array([np.average(SignalXA,axis=1), np.average(SignalYA,axis=1), np.average(SignalZA,axis=1),np.average(SignalXG,axis=1), np.average(SignalYG,axis=1), np.average(SignalZG,axis=1)])
    # Plotting for each signal axis
    plt.figure()
    # Plotting 'model' template for the particular class - both methods
    plt.plot(Signal_prealignment.T)
    plt.title('Average Signal')
    plt.legend(['Acc. X', 'Acc. Y', 'Acc. Z','Gyro X', 'Gyro Y', 'Gyro Z'])
    plt.xlabel('Sample No.')
    plt.ylabel('Value')
    plt.show()
    # for axis in ['X', 'Y', 'Z']:
    #     plt.figure()
    #     plt.title(f'Gyro {axis} Pre-Alignment')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}G[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Gyro {axis}'], loc='upper right')
    #         else:
    #             pass

    #     plt.figure()
    #     plt.title(f'Accel {axis} Pre-Alignment')
    #     for j in range(0, num, 1):
    #         plt.plot(SignalGraph, eval(f'Signal{axis}A[:,j]'), 'r')
    #         if j == 0:
    #             plt.legend([f'Accel {axis}'], loc='upper right')
    #         else:
    #             pass

    
    # lag values could be from -size+1 (smallest overlap on LHS) to size-timestep (smallest overlap on RHS)
    # lag_values = np.arange(-size+1, size, 1)
    # m = SignalXG.shape # Shot Martrix Shape (data points x no. of shots)
    
    # global lag
    # # Pairs of signals are combined and the cross correlation is evalauted
    # # The two signals are realigned and averaged
    # # This iterative process keeps repeating until one template signal is left - therefore must start with power of 2 shots
    
    # if num >= 64:
    
    #     path = np.array([32,16,8,4,2])
    #     avg_prop = np.zeros([32,size,6])
    #     avg_prop2 = np.zeros([16,size,6])
    #     avg_prop3 = np.zeros([8,size,6])
    #     avg_prop4 = np.zeros([4,size,6])
    #     avg_prop5 = np.zeros([2,size,6])

    #     for j in path:

    #         correlation = np.zeros([j,m[0]*2-1, 6])
    #         lag = np.zeros([j,6])
    #         max_crosscorr = np.zeros([j,6])

    #         for i in range(0,2*j,2):

    #             n = int(i/2)

    #             if j == 32:

    #                 correlation[n,:,0] = signal.correlate(SignalXG[:,i], SignalXG[:,i+1])
    #                 correlation[n,:,1] = signal.correlate(SignalYG[:,i], SignalYG[:,i+1])
    #                 correlation[n,:,2] = signal.correlate(SignalZG[:,i], SignalZG[:,i+1])
    #                 correlation[n,:,3] = signal.correlate(SignalXA[:,i], SignalXA[:,i+1])
    #                 correlation[n,:,4] = signal.correlate(SignalYA[:,i], SignalYA[:,i+1])
    #                 correlation[n,:,5] = signal.correlate(SignalZA[:,i], SignalZA[:,i+1])

    #                 max_crosscorr = np.argmax(correlation[n,:,:], axis=0)
    #                 lag[n,:] = lag_values[max_crosscorr]

    #                 SignalXG[:,i+1] = shift(SignalXG[:,i+1], -1*lag[n,0], cval=0)
    #                 SignalYG[:,i+1] = shift(SignalYG[:,i+1], -1*lag[n,1], cval=0)
    #                 SignalZG[:,i+1] = shift(SignalZG[:,i+1], -1*lag[n,2], cval=0)
    #                 SignalXA[:,i+1] = shift(SignalXA[:,i+1], -1*lag[n,3], cval=0)
    #                 SignalYA[:,i+1] = shift(SignalYA[:,i+1], -1*lag[n,4], cval=0)
    #                 SignalZA[:,i+1] = shift(SignalZA[:,i+1], -1*lag[n,5], cval=0)

    #                 avg_prop[n,:,0] = np.average(SignalXG[:,i:i+1], axis=1)
    #                 avg_prop[n,:,1] = np.average(SignalYG[:,i:i+1], axis=1)
    #                 avg_prop[n,:,2] = np.average(SignalZG[:,i:i+1], axis=1)
    #                 avg_prop[n,:,3] = np.average(SignalXA[:,i:i+1], axis=1)
    #                 avg_prop[n,:,4] = np.average(SignalYA[:,i:i+1], axis=1)
    #                 avg_prop[n,:,5] = np.average(SignalZA[:,i:i+1], axis=1)

    #             elif j == 16:

    #                 correlation[n,:,0] = signal.correlate(avg_prop[i,:,0], avg_prop[i+1,:,0])
    #                 correlation[n,:,1] = signal.correlate(avg_prop[i,:,1], avg_prop[i+1,:,1])
    #                 correlation[n,:,2] = signal.correlate(avg_prop[i,:,2], avg_prop[i+1,:,2])
    #                 correlation[n,:,3] = signal.correlate(avg_prop[i,:,3], avg_prop[i+1,:,3])
    #                 correlation[n,:,4] = signal.correlate(avg_prop[i,:,4], avg_prop[i+1,:,4])
    #                 correlation[n,:,5] = signal.correlate(avg_prop[i,:,5], avg_prop[i+1,:,5])

    #                 max_crosscorr = np.argmax(correlation[n,:,:], axis=0)
    #                 lag[n,:] = lag_values[max_crosscorr]

    #                 avg_prop[i+1,:,0] = shift(avg_prop[i+1,:,0], -1*lag[n,0], cval=0)
    #                 avg_prop[i+1,:,1] = shift(avg_prop[i+1,:,1], -1*lag[n,1], cval=0)
    #                 avg_prop[i+1,:,2] = shift(avg_prop[i+1,:,2], -1*lag[n,2], cval=0)
    #                 avg_prop[i+1,:,3] = shift(avg_prop[i+1,:,3], -1*lag[n,3], cval=0)
    #                 avg_prop[i+1,:,4] = shift(avg_prop[i+1,:,4], -1*lag[n,4], cval=0)
    #                 avg_prop[i+1,:,5] = shift(avg_prop[i+1,:,5], -1*lag[n,5], cval=0)

    #                 avg_prop2[n,:,:] = np.average(avg_prop[i:i+1,:,:], axis=0)

    #             elif j == 8:

    #                 correlation[n,:,0] = signal.correlate(avg_prop2[i,:,0], avg_prop2[i+1,:,0])
    #                 correlation[n,:,1] = signal.correlate(avg_prop2[i,:,1], avg_prop2[i+1,:,1])
    #                 correlation[n,:,2] = signal.correlate(avg_prop2[i,:,2], avg_prop2[i+1,:,2])
    #                 correlation[n,:,3] = signal.correlate(avg_prop2[i,:,3], avg_prop2[i+1,:,3])
    #                 correlation[n,:,4] = signal.correlate(avg_prop2[i,:,4], avg_prop2[i+1,:,4])
    #                 correlation[n,:,5] = signal.correlate(avg_prop2[i,:,5], avg_prop2[i+1,:,5])

    #                 max_crosscorr = np.argmax(correlation[n,:,:], axis=0)
    #                 lag[n,:] = lag_values[max_crosscorr]

    #                 avg_prop2[i+1,:,0] = shift(avg_prop2[i+1,:,0], -1*lag[n,0], cval=0)
    #                 avg_prop2[i+1,:,1] = shift(avg_prop2[i+1,:,1], -1*lag[n,1], cval=0)
    #                 avg_prop2[i+1,:,2] = shift(avg_prop2[i+1,:,2], -1*lag[n,2], cval=0)
    #                 avg_prop2[i+1,:,3] = shift(avg_prop2[i+1,:,3], -1*lag[n,3], cval=0)
    #                 avg_prop2[i+1,:,4] = shift(avg_prop2[i+1,:,4], -1*lag[n,4], cval=0)
    #                 avg_prop2[i+1,:,5] = shift(avg_prop2[i+1,:,5], -1*lag[n,5], cval=0)

    #                 avg_prop3[n,:,:] = np.average(avg_prop2[i:i+1, :,:], axis=0)
                    
                    
    #             elif j == 4:

    #                 correlation[n,:,0] = signal.correlate(avg_prop3[i,:,0], avg_prop3[i+1,:,0])
    #                 correlation[n,:,1] = signal.correlate(avg_prop3[i,:,1], avg_prop3[i+1,:,1])
    #                 correlation[n,:,2] = signal.correlate(avg_prop3[i,:,2], avg_prop3[i+1,:,2])
    #                 correlation[n,:,3] = signal.correlate(avg_prop3[i,:,3], avg_prop3[i+1,:,3])
    #                 correlation[n,:,4] = signal.correlate(avg_prop3[i,:,4], avg_prop3[i+1,:,4])
    #                 correlation[n,:,5] = signal.correlate(avg_prop3[i,:,5], avg_prop3[i+1,:,5])

    #                 max_crosscorr = np.argmax(correlation[n,:,:], axis=0)
    #                 lag[n,:] = lag_values[max_crosscorr]

    #                 avg_prop3[i+1,:,0] = shift(avg_prop3[i+1,:,0], -1*lag[n,0], cval=0)
    #                 avg_prop3[i+1,:,1] = shift(avg_prop3[i+1,:,1], -1*lag[n,1], cval=0)
    #                 avg_prop3[i+1,:,2] = shift(avg_prop3[i+1,:,2], -1*lag[n,2], cval=0)
    #                 avg_prop3[i+1,:,3] = shift(avg_prop3[i+1,:,3], -1*lag[n,3], cval=0)
    #                 avg_prop3[i+1,:,4] = shift(avg_prop3[i+1,:,4], -1*lag[n,4], cval=0)
    #                 avg_prop3[i+1,:,5] = shift(avg_prop3[i+1,:,5], -1*lag[n,5], cval=0)

    #                 avg_prop4[n,:,:] = np.average(avg_prop3[i:i+1, :,:], axis=0)
                    
                
    #             elif j == 2:

    #                 correlation[n,:,0] = signal.correlate(avg_prop4[i,:,0], avg_prop4[i+1,:,0])
    #                 correlation[n,:,1] = signal.correlate(avg_prop4[i,:,1], avg_prop4[i+1,:,1])
    #                 correlation[n,:,2] = signal.correlate(avg_prop4[i,:,2], avg_prop4[i+1,:,2])
    #                 correlation[n,:,3] = signal.correlate(avg_prop4[i,:,3], avg_prop4[i+1,:,3])
    #                 correlation[n,:,4] = signal.correlate(avg_prop4[i,:,4], avg_prop4[i+1,:,4])
    #                 correlation[n,:,5] = signal.correlate(avg_prop4[i,:,5], avg_prop4[i+1,:,5])

    #                 max_crosscorr = np.argmax(correlation[n,:,:], axis=0)
    #                 lag[n,:] = lag_values[max_crosscorr]

    #                 avg_prop4[i+1,:,0] = shift(avg_prop4[i+1,:,0], -1*lag[n,0], cval=0)
    #                 avg_prop4[i+1,:,1] = shift(avg_prop4[i+1,:,1], -1*lag[n,1], cval=0)
    #                 avg_prop4[i+1,:,2] = shift(avg_prop4[i+1,:,2], -1*lag[n,2], cval=0)
    #                 avg_prop4[i+1,:,3] = shift(avg_prop4[i+1,:,3], -1*lag[n,3], cval=0)
    #                 avg_prop4[i+1,:,4] = shift(avg_prop4[i+1,:,4], -1*lag[n,4], cval=0)
    #                 avg_prop4[i+1,:,5] = shift(avg_prop4[i+1,:,5], -1*lag[n,5], cval=0)

    #                 avg_prop5[n,:,:] = np.average(avg_prop4[i:i+1, :,:], axis=0)

                    

    #     # Final Template
    #     lag = np.zeros([6])
    #     correlation_XG4 = np.zeros([6,m[0]*2-1])

    #     correlation_XG4[0,:] = signal.correlate(avg_prop5[0,:,0], avg_prop5[1,:,0])
    #     correlation_XG4[1,:] = signal.correlate(avg_prop5[0,:,1], avg_prop5[1,:,1])
    #     correlation_XG4[2,:] = signal.correlate(avg_prop5[0,:,2], avg_prop5[1,:,2])
    #     correlation_XG4[3,:] = signal.correlate(avg_prop5[0,:,3], avg_prop5[1,:,3])
    #     correlation_XG4[4,:] = signal.correlate(avg_prop5[0,:,4], avg_prop5[1,:,4])
    #     correlation_XG4[5,:] = signal.correlate(avg_prop5[0,:,5], avg_prop5[1,:,5])


    #     max_crosscorr_xg = np.argmax(correlation_XG4, axis = 1)
    #     lag = lag_values[max_crosscorr_xg]

    #     avg_prop5[1,:,0] = shift(avg_prop5[1,:,0], -1*lag[0], cval=0)
    #     avg_prop5[1,:,1] = shift(avg_prop5[1,:,1], -1*lag[1], cval=0)
    #     avg_prop5[1,:,2] = shift(avg_prop5[1,:,2], -1*lag[2], cval=0)
    #     avg_prop5[1,:,3] = shift(avg_prop5[1,:,3], -1*lag[3], cval=0)
    #     avg_prop5[1,:,4] = shift(avg_prop5[1,:,4], -1*lag[4], cval=0)
    #     avg_prop5[1,:,5] = shift(avg_prop5[1,:,5], -1*lag[5], cval=0)

    #     template = np.average(avg_prop5, axis=0)
    #     # print(template.shape)
        
    #     plt.figure()
    #     # Plotting 'model' template for the particular class - both methods
    #     plt.plot(template)
    #     plt.title('Average Signal')
    #     plt.legend(['Gyro X', 'Gyro Y', 'Gyro Z', 'Acc. X', 'Acc. Y', 'Acc. Z'])
    #     plt.xlabel('Sample No.')
    #     plt.ylabel('Value')
    #     plt.show()


    #     shots_aligned = np.zeros([m[1],m[0]*2-1, 6])
    #     lag = np.zeros([m[1],6])
    #     max_crosscorr = np.zeros([m[1],6])

    #     for i in range(0,m[1]):

    #         shots_aligned[i,:,0] = signal.correlate(SignalXG[:,i], template[:,0])
    #         shots_aligned[i,:,1] = signal.correlate(SignalYG[:,i], template[:,1])
    #         shots_aligned[i,:,2] = signal.correlate(SignalZG[:,i], template[:,2])
    #         shots_aligned[i,:,3] = signal.correlate(SignalXA[:,i], template[:,3])
    #         shots_aligned[i,:,4] = signal.correlate(SignalYA[:,i], template[:,4])
    #         shots_aligned[i,:,5] = signal.correlate(SignalZA[:,i], template[:,5])

    #         max_crosscorr = np.argmax(shots_aligned[i,:,:], axis=0)
    #         lag[i,:] = lag_values[max_crosscorr]

    #         SignalXG[:,i] = shift(SignalXG[:,i], -1*lag[i,0], cval=0)
    #         SignalYG[:,i] = shift(SignalYG[:,i], -1*lag[i,1], cval=0)
    #         SignalZG[:,i] = shift(SignalZG[:,i], -1*lag[i,2], cval=0)
    #         SignalXA[:,i] = shift(SignalXA[:,i], -1*lag[i,3], cval=0)
    #         SignalYA[:,i] = shift(SignalYA[:,i], -1*lag[i,4], cval=0)
    #         SignalZA[:,i] = shift(SignalZA[:,i], -1*lag[i,5], cval=0)  
    #     # # Plotting for each signal axis
    #     # for axis in ['X', 'Y', 'Z']:
    #     #     plt.figure()
    #     #     plt.title(f'Gyro {axis} Aligned')
    #     #     for j in range(0, num, 1):
    #     #         plt.plot(SignalGraph, eval(f'Signal{axis}G[:,j]'), 'r')
    #     #         if j == 0:
    #     #             plt.legend([f'Gyro {axis}'], loc='upper right')
    #     #         else:
    #     #             pass

    #     #     plt.figure()
    #     #     plt.title(f'Accel {axis} Aligned')
    #     #     for j in range(0, num, 1):
    #     #         plt.plot(SignalGraph, eval(f'Signal{axis}A[:,j]'), 'r')
    #     #         if j == 0:
    #     #             plt.legend([f'Accel {axis}'], loc='upper right')
    #     #         else:
    #     #             pass
    #     return SignalXG, SignalYG, SignalZG, SignalXA, SignalYA, SignalZA,template
    
    return Signal_prealignment #SignalXG, SignalYG, SignalZG, SignalXA, SignalYA, SignalZA

def readfilesinfolder(path,stroke_category= 5):
    # global labels
    if stroke_category== 5:
        shot_index= ['Fore','Back','ForeV','BackV','Serve']
        shots= [[],[],[],[],[]]
    elif stroke_category== 3:
        shot_index= ['Fore','Back','Serve']
        shots= [[],[],[]]
    elif stroke_category== 4:
        shot_index= ['Fore','Back','Volley','Serve']
        shots= [[],[],[],[]]
    # labels= shot_index
    shots_made=0
   
    for root, dirs, files in os.walk(path):
            for file in files:
                    if 'Motion' in file and '.csv' in file and 'Henry' not in root:
                        shot_type= root.split('Sensor/')[1].split('_')[0]
                        shots_made += int(root.split(f'{shot_type}_')[1].split('_')[0])
                        #because os on windows mixes the slashes up
                        file_path= os.path.join(root, file).replace("\\","/")
                        #so that volley combines to it's respective forehand and backhand
                        if stroke_category== 3:
                            if shot_type== 'ForeV' or shot_type== 'BackV':
                                shot_type = shot_type[:-1]
                        elif stroke_category ==4:
                            if shot_type== 'ForeV' or shot_type== 'BackV':
                                shot_type = 'Volley'
                        shots[shot_index.index(shot_type)] += [file_path]

     
                    
    return shots, shots_made      
#%%
path_windows= '/Users/wwo20/OneDrive - Imperial College London/'
path_mac= '/Users/wisdom/Library/CloudStorage/OneDrive-ImperialCollegeLondon/'
path= path_mac
shot_filenames_list,shots_made= readfilesinfolder(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Watch Sensor/')
players= ['Josh','Smriti','Tom','Fran','Wisdom','Kareena','Amber','Oliver','Henry']
shots_type = ['Fore','ForeV','Back','BackV','Serve']
# Josh= {'name': 'Josh', 'Serve_Rot':[]}

forehand_csv_temp= pd.read_csv(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/Henry_Template/Fore_template.csv').to_numpy()
backhand_csv_temp= pd.read_csv(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/Henry_Template/Back_template.csv').to_numpy()
serve_csv_temp= pd.read_csv(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/Henry_Template/Serve_template.csv').to_numpy()
forehandvolley_csv_temp= pd.read_csv(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/Henry_Template//ForeV_template.csv').to_numpy()
backhandvolley_csv_temp= pd.read_csv(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/Henry_Template/BackV_template.csv').to_numpy()
#%%
# shot_filenames_list,shots_made= readfilesinfolder(f'{path}uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Watch Sensor/')
disha_datapath= f'{path}/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Data/'
disha_forev_filepaths= [f'{disha_datapath}00858_CalInertialAndMag.csv', f'{disha_datapath}00860_CalInertialAndMag.csv']
disha_backv_filepaths= [f'{disha_datapath}00859_CalInertialAndMag.csv', f'{disha_datapath}00862_CalInertialAndMag.csv']
disha_serve_filepaths= [f'{disha_datapath}00057_CalInertialAndMag.csv', f'{disha_datapath}00067_CalInertialAndMag.csv', f'{disha_datapath}00070_CalInertialAndMag.csv']

#forehands
AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ,Allfpitch, AllfRoll,Allfyaw,Allfname,Allfshot,Allfshots_made = Compile(shot_filenames_list[0])
# AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ = cross_corr(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
# fore_template= cross_corr(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
faMax, faMin, faMean, faStd, faArea, fgMax, fgMin, fgMean, fgStd, fgArea = MaxMin(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
AllfGyro_av, AllfAccel_av, LinSpeeds, thetah_f, thetal_f, magAlow_f, magAhigh_f =feature_template(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ,Allfname,Allfpitch, AllfRoll,Allfyaw,Allfshot,forehand_csv_temp)

#backhands
AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ,Allbpitch, AllbRoll,Allbyaw,Allbname,Allbshot,Allbshots_made = Compile(shot_filenames_list[1])
# AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ = cross_corr(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ,128)
# back_template= cross_corr(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
baMax,baMin,baMean,baStd,baArea,bgMax,bgMin,bgMean,bgStd,bgArea = MaxMin(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
AllbGyro_av, AllbAccel_av, LinSpeeds, thetah_b, thetal_b, magAlow_b, magAhigh_b =feature_template(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ,Allbname,Allbpitch, AllbRoll,Allbyaw,Allbshot,backhand_csv_temp)

#volley backhands
AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ,Allvbpitch, AllvbRoll,Allvbyaw,Allvbname,Allvbshot,Allvbshots_made = Compile(shot_filenames_list[3])
# AllbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ = cross_corr(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ)
# volleyback_template= cross_corr(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ)
vbaMax, vbaMin, vbaMean, vbaStd, vbaArea, vbgMax, vbgMin, vbgMean, vbgStd, vbgArea = MaxMin(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ)
AllvbGyro_av, AllvbAccel_av, LinSpeedvb, thetah_vb, thetal_vb, magAlow_vb, magAhigh_vb = feature_template(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ,Allvbname,Allvbpitch, AllvbRoll,Allvbyaw,Allvbshot,backhandvolley_csv_temp)

#volleuyfrehands
AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ,Allvfpitch, AllvfRoll,Allvfyaw,Allvfname,Allvfshot,Allvfshots_made = Compile(shot_filenames_list[2])
# AllbGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ = cross_corr(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ)
# volley_fore_template= cross_corr(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ)
vfaMax, vfaMin, vfaMean, vfaStd, vfaArea, vfgMax, vfgMin, vfgMean, vfgStd, vfgArea = MaxMin(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ)
AllvfGyro_av, AllvfAccel_av, LinSpeedvf, thetah_vf, thetal_vf, magAlow_vf, magAhigh_vf = feature_template(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ,Allvfname,Allvfpitch, AllvfRoll,Allvfyaw,Allvfshot,forehandvolley_csv_temp)

#serves
AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ,Allspitch, AllsRoll,Allsyaw,Allsname,Allsshot,Allsshots_made = Compile(shot_filenames_list[4])
# AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ = cross_corr(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ)
# serve_template= cross_corr(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ)
saMax, saMin, saMean, saStd, saArea, sgMax, sgMin, sgMean, sgStd, sgArea = MaxMin(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ)
AllsGyro_av, AllsAccel_av, LinSpeeds, thetah_s, thetal_s, magAlow_s, magAhigh_s =feature_template(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ,Allsname,Allspitch, AllsRoll,Allsyaw,Allsshot,serve_csv_temp)

#%%
aMaxAll = np.vstack((faMax, vfaMax, baMax, vbaMax, saMax))
aMinAll = np.vstack((faMin, vfaMin, baMin, vbaMin, saMin))
aMeanAll = np.vstack((faMean, vfaMean, baMean, vbaMean, saMean))
aStdAll = np.vstack((faStd, vfaStd, baStd, vbaStd, saStd))
aAreaAll = np.vstack((faArea, vfaArea, baArea, vbaArea, saArea))
gMinAll = np.vstack((fgMin, vfgMin, bgMin, vbgMin, sgMin))
gMaxAll = np.vstack((fgMax, vfgMax, bgMax, vbgMax, sgMax))
gMeanAll = np.vstack((fgMean, vfgMean, bgMean, vbgMean, sgMean))
gStdAll = np.vstack((fgStd, vfgStd, bgStd, vbgStd, sgStd))
gAreaAll = np.vstack((fgArea, vfgArea, bgArea, vbgArea, sgArea))
fA = np.hstack((aMaxAll, aMinAll, aMeanAll, aStdAll, aAreaAll, gMinAll, gMaxAll, gMeanAll, gStdAll, gAreaAll))

shots_made_array= np.hstack((np.sum(Allfshots_made),np.sum(Allvfshots_made),np.sum(Allbshots_made),np.sum(Allvbshots_made),np.sum(Allsshots_made)))
shots_detected= np.hstack((AllfGyroX.shape[1],AllvfGyroX.shape[1],AllbGyroX.shape[1],AllvbGyroX.shape[1],AllsGyroX.shape[1]))
#tp make sure bars dont overlap s
width=0.25
r=np.arange(5)
plt.bar(r,shots_made_array,width=width,label= 'Shots made')
plt.bar(5,shots_made,width=width)
plt.bar(r+width,shots_detected,width=width,label= 'Shots detected')
plt.bar(5+width,aAreaAll.shape[0],width=width)
plt.xticks(np.hstack((r,5))+width/2,shots_type+['Total'])
plt.title(f'Detection accuracy {np.round((aAreaAll.shape[0]/shots_made)*100,2)}%')
plt.legend()
plt.show()
# %%
