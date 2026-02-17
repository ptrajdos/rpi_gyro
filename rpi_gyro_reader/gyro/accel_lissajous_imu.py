import math

import numpy as np
from rpi_gyro_reader.gyro.iimu import IMU
import numpy as np


class AccelLissajousIMU(IMU):
    """Simulates a moving IMU for testing"""

    def __init__(self, dt=0.01, A=3.0, B=4.0, wx=3.0, wy=4.0, shift=0.0):
        self.t = 0.0
        self.dt = dt
        self.A = A
        self.B = B
        self.wx = wx
        self.wy = wy
        self.shift = shift

    def read_accel(self):
        

        ax = -self.A * (self.wx**2) * np.sin(self.wx*self.t)
        ay = -self.B * (self.wy**2) * np.sin(self.wy*self.t + self.shift)
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
