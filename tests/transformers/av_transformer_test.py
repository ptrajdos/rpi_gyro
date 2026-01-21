
from rpi_gyro_reader.transformers.av_transformer import AVTransformer
from tests.transformers.itransformer_test import ITransformerTest


class AVTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": AVTransformer()}
