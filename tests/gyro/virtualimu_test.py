from rpi_gyro_reader.gyro.virtualimu import VirtualIMU
from tests.gyro.iimu_test import IMUTest


class VirtualImuTest(IMUTest):
    
    __test__ = True

    def get_imu(self):
        return VirtualIMU()