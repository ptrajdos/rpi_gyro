from rpi_gyro_reader.transformers.cursor_movers.acc_velocity_mover import AccVelocityMover
from tests.transformers.itransformer_test import ITransformerTest


class PassTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": AccVelocityMover()}
