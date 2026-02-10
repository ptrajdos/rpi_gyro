from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover
from rpi_gyro_reader.transformers.cursor_movers.kalman_mover import KalmanMover
from tests.transformers.itransformer_test import ITransformerTest


class KalmanMoverTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": KalmanMover()}
