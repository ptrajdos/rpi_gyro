import abc

class IMU(abc.ABC):
    @abc.abstractmethod
    def read_accel(self) -> tuple[float, float, float]:
        """Return X, Y, Z acceleration (m/s²)"""
        pass

    @abc.abstractmethod
    def read_gyro(self) -> tuple[float, float, float]:
        """Return X, Y, Z rotation (deg/s)"""
        pass

    @abc.abstractmethod
    def read_motion(self) -> tuple[float, float, float, float, float, float]:
        """Return accel + gyro together

        Returns:
        Tuple with values
        (aX, aY, aZ, gX, gY, gZ) 
        """
        pass
