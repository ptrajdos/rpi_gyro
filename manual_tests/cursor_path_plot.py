import numpy as np
from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover

from matplotlib import pyplot as plt
import pyautogui


def main():
    n_samples = 1000
    imu = AccelCircleIMU()
    vel_mover = AccVelocityMover()

    accs = np.zeros((n_samples, 2))
    deltas = np.zeros((n_samples, 2))
    positions = []

    delta_pix = 3000

    last_pos = np.zeros(2)

    for i in range(n_samples):
        print("moving")
        vec = imu.read_accel()
        accs[i] = vec[0:2]
        delta = vel_mover.transform_sample(vec)
        delta*=delta_pix
        # pyautogui.moveRel(delta[0], delta[1], duration=0.001)
        last_pos += delta
        deltas[i] = delta.copy()
        positions.append(last_pos.copy())

    positions = np.asanyarray(positions)
    
    plt.subplot(1,3,1)
    plt.plot(accs[:,0])
    plt.plot(accs[:,1])

    plt.subplot(1,3,2)
    plt.plot(positions[:,0],positions[:,1])

    plt.subplot(1,3,3)
    plt.plot(deltas[:,0],deltas[:,1])

    plt.show()






if __name__ == '__main__':
    main()