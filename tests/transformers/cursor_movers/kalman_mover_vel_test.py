
from rpi_gyro_reader.transformers.cursor_movers.kalman_mover_vel import KalmanMoverVel
from tests.transformers.itransformer_test import ITransformerTest


class KalmanMoverVelTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": KalmanMoverVel()}
