import abc
import numpy as np
class IMU(abc.ABC):
    #TODO return numpy array instead of tuple?
    @abc.abstractmethod
    def read_accel(self) -> np.ndarray:
        """Return X, Y, Z acceleration (m/s²)"""
        pass

    @abc.abstractmethod
    def read_gyro(self) -> np.ndarray:
        """Return X, Y, Z rotation (deg/s)"""
        pass

    #TODO read magnetometer?

    @abc.abstractmethod
    def read_motion(self) -> np.ndarray:
        """Return accel + gyro together

        Returns:
        Numpy array with values
        [aX, aY, aZ, gX, gY, gZ]
        """
        pass
