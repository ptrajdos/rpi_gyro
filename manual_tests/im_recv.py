
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver


def main():
    rcv = IMUReceiver(address="localhost")
    print("Receiving...")
    try:
        while True:
            ax, ay, az, gx, gy, gz = rcv.read_motion()
            print(f"{ax}, {ay}, {az}, {gx}, {gy}, {gz}")
    except KeyboardInterrupt:
        rcv.stop()
        print("Done")


if __name__ == "__main__":
    main()