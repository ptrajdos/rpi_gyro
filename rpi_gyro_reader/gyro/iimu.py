import abc
import numpy as np
class IMU(abc.ABC):
    @abc.abstractmethod
    def read_accel(self) -> np.ndarray:
        """Return X, Y, Z acceleration (m/s²)"""
        pass

    @abc.abstractmethod
    def read_gyro(self) -> np.ndarray:
        """Return X, Y, Z rotation (deg/s)"""
        pass

    @abc.abstractmethod
    def read_mag(self) -> np.ndarray:
        """Return X, Y, Z magnetic field (uT)"""
        pass

    @abc.abstractmethod
    def read_motion(self) -> np.ndarray:
        """Return accel + gyro together

        Returns:
        Numpy array with values
        [aX, aY, aZ, gX, gY, gZ, mX, mY, mZ]
        """
        pass
