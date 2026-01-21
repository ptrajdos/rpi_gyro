
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
import numpy as np
import time

def main():
    rcv = IMUReceiver(address="localhost")
    trans = AVTransformer()
    print("Receiving...")
    try:
        while True:
            ax, ay, az, gx, gy, gz = rcv.read_motion()
            axt, ayt, azt, gxt, gyt, gzt = trans.transform_sample(np.asanyarray((ax, ay, az, gx, gy, gz)))
            print(f"R: {ax}, {ay}, {az}, {gx}, {gy}, {gz}")
            print(f"T: {axt}, {ayt}, {azt}, {gxt}, {gyt}, {gzt}")
            time.sleep(1)
    except KeyboardInterrupt:
        rcv.stop()
        print("Done")


if __name__ == "__main__":
    main()