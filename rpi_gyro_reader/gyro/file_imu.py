import math

import numpy as np
from rpi_gyro_reader.gyro.iimu import IMU
import numpy as np
import pandas as pd


class FileIMU(IMU):
    """Simulates a moving IMU for testing"""

    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path, header=0)
        self._gen = self.df.iterrows()

    def read_accel(self):
        try:
            _, row = next(self._gen)
            return np.array([row["ax"], row["ay"], row["az"]])
        except StopIteration:
            self._gen = self.df.iterrows()
            _, row = next(self._gen)
            return np.array([row["ax"], row["ay"], row["az"]])

    def read_gyro(self):
        try:
            _, row = next(self._gen)
            return np.array([row["gx"], row["gy"], row["gz"]])
        except StopIteration:
            self._gen = self.df.iterrows()
            _, row = next(self._gen)
            return np.array([row["gx"], row["gy"], row["gz"]])

    def read_motion(self):
        try:
            _, row = next(self._gen)
            return np.array(
                [
                    row["ax"],
                    row["ay"],
                    row["az"],
                    row["gx"],
                    row["gy"],
                    row["gz"],
                    row["mx"],
                    row["my"],
                    row["mz"],
                ]
            )
        except StopIteration:
            self._gen = self.df.iterrows()
            _, row = next(self._gen)
            return np.array(
                [
                    row["ax"],
                    row["ay"],
                    row["az"],
                    row["gx"],
                    row["gy"],
                    row["gz"],
                    row["mx"],
                    row["my"],
                    row["mz"],
                ]
            )

    def read_mag(self):
        try:
            _, row = next(self._gen)
            return np.array([row["mx"], row["my"], row["mz"]])
        except StopIteration:
            self._gen = self.df.iterrows()
            _, row = next(self._gen)
            return np.array([row["mx"], row["my"], row["mz"]])
