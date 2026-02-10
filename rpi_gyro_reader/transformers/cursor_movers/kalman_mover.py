import numpy as np
from rpi_gyro_reader.transformers.cursor_movers.icursormover import CursorMover


class KalmanMover(CursorMover):
    def __init__(self, dt=0.01, alpha=0.95):
        super().__init__()
        self.dt = dt
        self.alpha = alpha
        self.reset()
        
        

    def reset(self):
        self.x = np.zeros((4, 1))  # state: vx, vy, ax, ay
        self.P = np.eye(4)

        
        self.F = np.array([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1],
        ])
        
        self.H = np.array([
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        qv = 1e-4
        qa = 1e-3
        self.Q = np.diag([qv, qv, qa, qa])

        r = 1e-1
        self.R = np.diag([r, r])

        self.I = np.eye(4)

    def _predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def _update(self, ax_meas, ay_meas):
        z = np.array([[ax_meas], [ay_meas]])
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (self.I - K @ self.H) @ self.P

    def _step(self, ax_meas, ay_meas):
        self._predict()
        self._update(ax_meas, ay_meas)
        return self.x.flatten()  #vx, vy, ax, ay

    def transform_sample(self, vec):
        ax, ay = vec[0], vec[1]
        state = self._step(ax, ay)
        delta = state[0:2] * self.dt  # Use velocity for movement
        delta *= self.alpha

        return delta

    def fit(self, X):
        return self