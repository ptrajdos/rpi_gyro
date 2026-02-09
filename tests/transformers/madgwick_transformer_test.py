from rpi_gyro_reader.transformers.madgwick_transformer import MadgwickTransformer
from rpi_gyro_reader.transformers.pass_transformer import PassTransformer
from tests.transformers.itransformer_test import ITransformerTest


class MagdwickTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {
            "Base": MadgwickTransformer(),
            "With Magnetometer": MadgwickTransformer(use_magnetometer=True),
            "Body Frame": MadgwickTransformer(return_body_frame=True),
            "Earth Frame": MadgwickTransformer(return_body_frame=False),
                }
