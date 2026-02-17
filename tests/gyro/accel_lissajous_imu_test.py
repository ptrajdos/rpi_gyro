from rpi_gyro_reader.gyro.accel_lissajous_imu import AccelLissajousIMU
from tests.gyro.iimu_test import IMUTest


class VirtualImuTest(IMUTest):
    
    __test__ = True

    def get_imu(self):
        return AccelLissajousIMU()