from rpi_gyro_reader.gyro.accel_circle_imu import AccelCircleIMU
from tests.gyro.iimu_test import IMUTest


class VirtualImuTest(IMUTest):
    
    __test__ = True

    def get_imu(self):
        return AccelCircleIMU()