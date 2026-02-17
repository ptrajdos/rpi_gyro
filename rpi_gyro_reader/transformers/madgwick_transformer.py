from rpi_gyro_reader.transformers.itransformer import ITransformer
import numpy as np
from ahrs.filters import Madgwick
from ahrs.common.orientation import q2euler, q2R


class MadgwickTransformer(ITransformer):

    def __init__(
        self,
        use_magnetometer=False,
        earth_magnetic_field=(0.0, 0.0, 9.81),
        return_body_frame=True,
    ):
        super().__init__()
        self.use_magnetometer = use_magnetometer
        self.earth_magnetic_field = earth_magnetic_field
        self.return_body_frame = return_body_frame

        self.reset()

    def transform_sample(self, vec):
        q = (
            self.magdwick.updateMARG(self.q, vec[:3], vec[3:6], vec[6:9])
            if self.use_magnetometer
            else self.magdwick.updateIMU(self.q, vec[:3], vec[3:6])
        )
        R = q2R(q)
        acc_linear = R @ vec[:3] - self.earth_magnetic_field

        if self.return_body_frame:
            acc_linear = R.T @ acc_linear
            return acc_linear
        
        return acc_linear

    def reset(self):
        self.magdwick = Madgwick()
        self.q = np.array([1.0, 0.0, 0.0, 0.0])

    def fit(self, X, y=None):
        return self
