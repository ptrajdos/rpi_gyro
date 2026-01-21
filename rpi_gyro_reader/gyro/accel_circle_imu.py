import math

import numpy as np
from rpi_gyro_reader.gyro.iimu import IMU


class AccelCircleIMU(IMU):
    """Simulates a moving IMU for testing"""

    def __init__(self, dt=0.01, radius=1.0, freq = 0.2):
        self.t = 0.0
        self.dt = dt
        self.radius = radius
        self.freq = freq


    def read_accel(self):
        omega = 2 * math.pi * self.freq
        
        ax = - (omega**2) * self.radius * np.cos(omega * self.t)
        ay = - (omega**2) * self.radius * np.sin(omega * self.t)
        az = 0

        self.t += self.dt
        return ax, ay, az

    def read_gyro(self):
        # Simulate slow rotation
        gx = 0
        gy = 0
        gz = 0
        self.t += 0.01
        return gx, gy, gz

    def read_motion(self):
        ax, ay, az  = self.read_gyro()
        
        gx = 0
        gy = 0
        gz = 0
        

        return (ax, ay, az, gx, gy, gz)
