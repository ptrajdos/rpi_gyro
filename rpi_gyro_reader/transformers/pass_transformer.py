from rpi_gyro_reader.transformers.itransformer import ITransformer


class PassTransformer(ITransformer):

    def transform_sample(self, vec):
        return vec

    def reset(self):
        pass

    def fit(self, X, y=None):
        return self