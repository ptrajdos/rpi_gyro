from rpi_gyro_reader.transformers.pass_transformer import PassTransformer
from tests.transformers.itransformer_test import ITransformerTest


class PassTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": PassTransformer()}
