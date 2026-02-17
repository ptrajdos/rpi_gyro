import numpy as np
from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.gyro.accel_lissajous_imu import AccelLissajousIMU
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover

from matplotlib import pyplot as plt
import pyautogui
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import time

from rpi_gyro_reader.transformers.cursor_movers.kalman_mover import KalmanMover
from rpi_gyro_reader.transformers.cursor_movers.kalman_mover_vel import KalmanMoverVel
from rpi_gyro_reader.transformers.madgwick_transformer import MadgwickTransformer

def main():
    imu = AccelLissajousIMU(dt=0.1,A=1.0, B=1.0,wx=1,wy=1,shift=np.pi/2.0) # IMUReceiver(address="localhost")
    av_trans = AVTransformer(alpha=0.9)
    madg_trans = MadgwickTransformer()
    vel_mover = AccVelocityMover(dt=1.0, alpha=0.9, threshold=0.05)
    # kalman_mover = KalmanMover(dt=1.0, alpha=0.9,threshold=0.01,sigma_r=1)
    kalman_mover = KalmanMoverVel(dt=1.0, alpha=0.8,threshold=1.0,sigma_r=1, sensitivity=0.01)

    accs = []
    deltas = []
    positions = []

    delta_pix = 1
    cursor_path_file_name = "cursor_path.pdf"

    accs_file_name = "cursor_accs.csv"
    positions_file_name = "cursor_positions.csv"
    deltas_file_name = "cursor_deltas.csv"

    last_pos = np.zeros(2)

    print ("Starting cursor path plotting test...")
    while True:
        try:
            vec = imu.read_motion()
            vec[3:6] = vec[0:3]
            # vec[1] = 0.0
            # vec[2] = np.random.normal(0, 1.0) # Add noise to Z accel
        
            # vec = madg_trans.transform_sample(vec)


            accs.append(vec[3:5])
            # delta = vel_mover.transform_sample(vec)
            delta = kalman_mover.transform_sample(vec)
            delta*=delta_pix
            # pyautogui.moveRel(delta[0], delta[1], duration=0.001)
            time.sleep(0.01)
            last_pos += delta
            deltas.append(delta.copy())
            positions.append(last_pos.copy())
        except KeyboardInterrupt:
            print("Stopping...")
            break

    positions = np.asanyarray(positions)
    accs = np.asanyarray(accs)
    deltas = np.asanyarray(deltas)

    print("Saving results...")
    pd.DataFrame(accs, columns=["ax", "ay"]).to_csv(accs_file_name, index=False)
    pd.DataFrame(positions, columns=["px", "py"]).to_csv(positions_file_name, index=False)
    pd.DataFrame(deltas, columns=["dx", "dy"]).to_csv(deltas_file_name, index=False)

    print("Plotting results...")    
    with PdfPages(cursor_path_file_name) as pdf:
        plt.figure(figsize=(12, 12))
        plt.subplot(1,3,1)
        plt.plot(accs[:,0], label="X accel")
        plt.plot(accs[:,1], label="Y accel")
        plt.legend()


        plt.subplot(1,3,2)
        plt.plot(positions[:,0],positions[:,1], label="Cursor Path in pixels")
        plt.legend()

        plt.subplot(1,3,3)
        plt.plot(deltas[:,0],deltas[:,1], label="Deltas in pixels")

        plt.legend()
        pdf.savefig()
        plt.close()
    






if __name__ == '__main__':
    main()