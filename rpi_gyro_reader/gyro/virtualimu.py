import math
from rpi_gyro_reader.gyro.iimu import IMU
import numpy as np

class VirtualIMU(IMU):
    """Simulates a moving IMU for testing"""
    def __init__(self, dt = 0.01):
        self.t = 0.0
        self.dt = dt


    def read_accel(self):
        # Simulate simple oscillating motion + gravity
        ax = 2.0 * math.sin(self.t)
        ay = 0.5 * math.cos(self.t)
        az = 9.81 + 0.2 * math.sin(self.t/2)  # gravity + small vertical motion

        self.t += self.dt
        return np.array([ax, ay, az])

    def read_gyro(self):
        # Simulate slow rotation
        gx = 10.0 * math.sin(self.t/3)
        gy = 5.0 * math.cos(self.t/4)
        gz = 2.0 * math.sin(self.t/5)
        self.t += self.dt
        return np.array([gx, gy, gz])
    
    def read_motion(self):
        ax = 2.0 * math.sin(self.t)
        ay = 0.5 * math.cos(self.t)
        az = 9.81 + 0.2 * math.sin(self.t/2)  # gravity + small vertical motion
        gx = 10.0 * math.sin(self.t/3)
        gy = 5.0 * math.cos(self.t/4)
        gz = 2.0 * math.sin(self.t/5)
        self.t += self.dt

        return np.array([ax, ay, az, gx, gy, gz])