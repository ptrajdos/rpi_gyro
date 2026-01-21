from rpi_gyro_reader.transformers.itransformer import ITransformer


class PassTransformer(ITransformer):

    def transform_sample(self, vec) -> tuple[float, float, float, float, float, float]:
        return vec

    def reset(self):
        pass