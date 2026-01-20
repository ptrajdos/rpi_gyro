from rpi_gyro_reader.gyro.imu_publisher import IMUPublisher
from rpi_gyro_reader.gyro.imu_receiver import IMUReceiver
from rpi_gyro_reader.gyro.virtualimu import VirtualIMU
from tests.gyro.iimu_test import IMUTest
from tests.test_tools import get_unused_port


class IMUReceiverTest(IMUTest):
    
    __test__ = True

    def setUp(self):
        self.address="localhost"
        self.port = get_unused_port()
        

        self.pub = IMUPublisher(imu=VirtualIMU(), address=self.address, port=self.port)

        return super().setUp()

    def tearDown(self):
        self.pub.stop()
        return super().tearDown()


    def get_imu(self):
        return IMUReceiver(address=self.address, port=self.port)