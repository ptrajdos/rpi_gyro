import numpy as np
from rpi_gyro_reader.transformers.cursor_movers.icursormover import CursorMover


class AccVelocityMover(CursorMover):
    def __init__(self, dt=0.01, alpha=0.95, threshold=0.05):
        super().__init__()
        self.dt = dt
        self.alpha = alpha
        self.threshold = threshold

        self.velocity = np.zeros(2)
        

    def reset(self):
        self.velocity = np.zeros(2)

    def transform_sample(self, vec):
        acc = np.where(np.abs(vec) > self.threshold, vec, 0)

        self.velocity = self.alpha * self.velocity + acc[0:2] * self.dt
        delta = self.velocity * self.dt

        return delta

    def fit(self, X, y=None):
        return self