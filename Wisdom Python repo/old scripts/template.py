import numpy as np
import matplotlib.pyplot as plt

def template(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ):
    # Angular Velocities
    AllfGyro_av = np.mean(np.array([AllfGyroX, AllfGyroY, AllfGyroZ]), axis=0)

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
    print(MagAccelmeans)
    if MagAccelmeans.size > 0:
        magA_low = np.min(MagAccelmeans[:], axis=0)
        magA_high = np.max(MagAccelmeans[:])
    else:
        magA_low = 0
        magA_high = 0

    return AllfGyro_av, AllfAccel_av, LinSpeed, theta_high, theta_low, magA_low, magA_high