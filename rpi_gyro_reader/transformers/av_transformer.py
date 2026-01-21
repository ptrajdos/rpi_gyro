from rpi_gyro_reader.transformers.itransformer import ITransformer
import numpy as np

class AVTransformer(ITransformer):

    def __init__(self, alpha=0.5):
        super().__init__()
        self.alpha = alpha

        self.corrections = None

    def fit(self, X):
        return super().fit(X)


    def transform_sample(self, vec):
        if self.corrections is None:
            self.corrections = np.zeros_like(vec)

        self.corrections = self.alpha * self.corrections + (1 - self.alpha) * vec

        n_vec = vec - self.corrections

        return n_vec
    
    def reset(self):
        self.corrections = None