#!/usr/bin/env python
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
            vec = rcv.read_motion()
            axt, ayt, azt, gxt, gyt, gzt = trans.transform_sample(vec)
            print(f"R: {vec[0]}, {vec[1]}, {vec[2]}, {vec[3]}, {vec[4]}, {vec[5]}")
            print(f"T: {axt}, {ayt}, {azt}, {gxt}, {gyt}, {gzt}")
            time.sleep(1)
    except KeyboardInterrupt:
        rcv.stop()
        print("Done")


if __name__ == "__main__":
    main()