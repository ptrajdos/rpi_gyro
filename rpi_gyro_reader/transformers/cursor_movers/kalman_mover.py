import numpy as np
from rpi_gyro_reader.transformers.cursor_movers.icursormover import CursorMover
from filterpy.kalman import KalmanFilter

class KalmanMover(CursorMover):
    def __init__(self, dt=0.01, alpha=0.90,sigma_v=1e-3, sigma_a=1e-1, sigma_r=1, threshold=0.05):
        super().__init__()
        self.dt = dt
        self.alpha = alpha
        self.threshold = threshold
        self.sigma_v = sigma_v
        self.sigma_a = sigma_a
        self.sigma_r = sigma_r
        self.reset()
        
    def reset(self):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)

        
        self.kf.F = np.array([
            [self.alpha, 0, self.dt, 0],
            [0, self.alpha, 0, self.dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1],
        ])
        
        self.kf.H = np.array([ # type: ignore
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        self.kf.Q = np.diag([self.sigma_v, self.sigma_v, self.sigma_a, self.sigma_a])

        self.kf.R = np.diag([self.sigma_r, self.sigma_r])


    def transform_sample(self, vec):
        z = np.array((vec[0], vec[1]))
        nm = np.abs(z) < self.threshold
        z[nm] = 0.0  # type: ignore

        self.kf.predict()
        self.kf.update(z)
        delta = self.kf.x[0:2] * self.dt
        
        return delta.flatten()

    def fit(self, X, y=None):
        return self