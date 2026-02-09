#!/usr/bin/env python
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
import numpy as np
import time
import pandas as pd

def main():
    rcv = IMUReceiver(address="localhost")
    trans = AVTransformer()
    print("Receiving...")
    results = []
    try:
        while True:
            vec = rcv.read_motion()
            axt, ayt, azt, gxt, gyt, gzt, mxt, myt, mzt = trans.transform_sample(vec)
            print(f"R: {vec[0]:.4f}, {vec[1]:.4f}, {vec[2]:.4f}, {vec[3]:.4f}, {vec[4]:.4f}, {vec[5]:.4f}, {vec[6]:.4f}, {vec[7]:.4f}, {vec[8]:.4f}")
            print(f"T: {axt:.4f}, {ayt:.4f}, {azt:.4f}, {gxt:.4f}, {gyt:.4f}, {gzt:.4f}, {mxt:.4f}, {myt:.4f}, {mzt:.4f}")
            results.append(vec)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        rcv.stop()
        print("Done")
        print(f"Collected {len(results)} samples")
        df = pd.DataFrame(results, columns=["ax", "ay", "az", "gx", "gy", "gz", "mx", "my", "mz"])
        df.to_csv("imu_samples.csv", index=False)


if __name__ == "__main__":
    main()