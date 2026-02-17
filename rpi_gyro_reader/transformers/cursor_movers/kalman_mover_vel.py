import numpy as np
from rpi_gyro_reader.transformers.cursor_movers.icursormover import CursorMover
from filterpy.kalman import KalmanFilter

class KalmanMoverVel(CursorMover):
    def __init__(self, dt=0.01, alpha=0.90,sigma_v=1e-3, sigma_r=1.0, sensitivity=1.0,  threshold=0.05):
        super().__init__()
        self.dt = dt
        self.alpha = alpha
        self.threshold = threshold
        self.sigma_v = sigma_v
        self.sigma_r = sigma_r
        self.sensitivity = sensitivity
        self.reset()
        
    def reset(self):
        self.kf = KalmanFilter(dim_x=2, dim_z=2)

        
        self.kf.F = np.eye(2) * self.alpha

        self.kf.B = np.eye(2) * self.sensitivity # type: ignore
        
        self.kf.H = np.eye(2) # type: ignore

        self.kf.Q = np.eye(2)* self.sigma_v

        self.kf.R = np.eye(2) * self.sigma_r


    def transform_sample(self, vec):
        if len(vec) < 6:
            return np.zeros((2,))
        u = np.array((vec[3], vec[4])).reshape((2,1))
        
        

        self.kf.predict(u)

        u_norm = np.linalg.norm(u)
        
        if u_norm < self.threshold:
            self.kf.update(np.array([0,0]))

        delta = self.kf.x[0:2] * self.dt
        
        return delta.flatten()

    def fit(self, X, y=None):
        return self