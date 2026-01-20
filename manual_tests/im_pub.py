
from rpi_gyro_reader.gyro.imu_publisher import IMUPublisher
from rpi_gyro_reader.gyro.virtualimu import VirtualIMU
import time

from rpi_gyro_reader.gyro.imu_bmi160 import IMUBMI160


def main():
    imu = VirtualIMU() # IMUBMI160()
    pub = IMUPublisher(imu=imu, address="*", delay=0.01)
    print("Publishing...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    

    pub.stop()
    print("Done")
    

if __name__ == "__main__":
    main()

