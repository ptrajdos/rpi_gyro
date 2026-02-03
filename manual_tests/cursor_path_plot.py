import numpy as np
from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover

from matplotlib import pyplot as plt
import pyautogui
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import time

def main():
    imu = AccelCircleIMU(radius=0.1, freq=0.5) # IMUReceiver(address="localhost")
    av_trans = AVTransformer(alpha=0.9)
    vel_mover = AccVelocityMover(dt=1.0, alpha=0.9, threshold=0.05)

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
            vec = imu.read_accel()
            #FIXME: something odd is happening with AVTransformer
            # vec = av_trans.transform_sample(np.asanyarray(vec)) 
            accs.append(vec[0:2])
            delta = vel_mover.transform_sample(vec)
            delta*=delta_pix
            pyautogui.moveRel(delta[0], delta[1], duration=0.001)
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