import os
from manual_tests.settings import DATA_PATH
from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from rpi_gyro_reader.gyro.file_imu import FileIMU
from tests.gyro.iimu_test import IMUTest


class FileIMUTest(IMUTest):
    
    __test__ = True

    def get_imu(self):
        path = os.path.join(DATA_PATH, "imu_samples_1.csv")
        return FileIMU(path=path)