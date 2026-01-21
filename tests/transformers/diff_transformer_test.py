
from rpi_gyro_reader.transformers.diff_transformer import DiffTransformer
from tests.transformers.itransformer_test import ITransformerTest


class AVTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {"Base": DiffTransformer()}
