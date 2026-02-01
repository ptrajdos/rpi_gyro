from rpi_gyro_reader.transformers.itransformer import ITransformer


class DiffTransformer(ITransformer):
    """
    Computes the difference between the current and the last sample.
    """

    def __init__(self):
        super().__init__()

        self.last_vec = None

    def fit(self, X):
        return super().fit(X)

    def transform_sample(self, vec):
        if self.last_vec is None:
            self.last_vec = vec
            return vec
        
        n_vec = vec - self.last_vec
        self.last_vec = vec

        return n_vec
    
    def reset(self):
        self.last_vec = None
        
        