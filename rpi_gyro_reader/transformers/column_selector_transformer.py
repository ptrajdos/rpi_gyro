from rpi_gyro_reader.transformers.itransformer import ITransformer


class ColumnSelectorTransformer(ITransformer):

    def __init__(self, columns = None):
        super().__init__()
        self.columns = columns


    def transform_sample(self, vec):
        if self.columns is not None:
            return vec[self.columns]
        
        return vec

    def reset(self):
        pass

    def fit(self, X, y=None):
        return self