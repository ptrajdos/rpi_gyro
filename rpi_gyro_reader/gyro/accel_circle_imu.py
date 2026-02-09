import math

import numpy as np
from rpi_gyro_reader.gyro.iimu import IMU
import numpy as np


class AccelCircleIMU(IMU):
    """Simulates a moving IMU for testing"""

    def __init__(self, dt=0.01, radius=1.0, freq=0.2):
        self.t = 0.0
        self.dt = dt
        self.radius = radius
        self.freq = freq

    def read_accel(self):
        omega = 2 * math.pi * self.freq

        ax = -(omega**2) * self.radius * np.cos(omega * self.t)
        ay = -(omega**2) * self.radius * np.sin(omega * self.t)
        az = 0

        self.t += self.dt
        return np.array([ax, ay, az])

    def read_gyro(self):
        # Simulate slow rotation
        gx = 0
        gy = 0
        gz = 0
        self.t += 0.01
        return np.array([gx, gy, gz])

    def read_motion(self):
        ax, ay, az = self.read_accel()

        gx = 0
        gy = 0
        gz = 0
        mx, my, mz = 0.0, 0.0, 0.0

        return np.array([ax, ay, az, gx, gy, gz, mx, my, mz])
    
    def read_mag(self):
        return np.array([0.0, 0.0, 0.0])
