import unittest
import numpy as np

from rpi_gyro_reader.gyro.iimu import IMU

class IMUTest(unittest.TestCase):

    __test__ = False

    @classmethod
    def setUpClass(cls):
        if not cls.__test__:
            raise unittest.SkipTest(
                f"{cls.__name__}: Skipping for condition __test__ = False"
            )

    def get_imu(self)-> IMU:
        pass

    def test_imu_a(self):
        imu = self.get_imu()

        vals = imu.read_accel()

        self.assertTrue(len(vals) == 3, "Wrong length of returned tuple")
        self.assertFalse(np.any(np.isnan(vals)), "Nans in result")
        self.assertFalse(np.any(np.isinf(vals)), "Infs in result")

    def test_imu_g(self):
        imu = self.get_imu()

        vals = imu.read_gyro()

        self.assertTrue(len(vals) == 3, "Wrong length of returned tuple")
        self.assertFalse(np.any(np.isnan(vals)), "Nans in result")
        self.assertFalse(np.any(np.isinf(vals)), "Infs in result")

    def test_imu_m(self):
        imu = self.get_imu()

        vals = imu.read_motion()

        self.assertTrue(len(vals) == 6, "Wrong length of returned tuple")
        self.assertFalse(np.any(np.isnan(vals)), "Nans in result")
        self.assertFalse(np.any(np.isinf(vals)), "Infs in result")



