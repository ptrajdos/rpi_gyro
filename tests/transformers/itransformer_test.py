from copy import deepcopy
import unittest
import numpy as np


class ITransformerTest(unittest.TestCase):

    __test__ = False

    @classmethod
    def setUpClass(cls):
        if not cls.__test__:
            raise unittest.SkipTest(
                f"{cls.__name__}: Skipping for condition __test__ = False"
            )

    def get_transformers(self):
        raise NotImplementedError

    def generate_sample_data(self, n_samples=10, n_cols=6):
        return np.random.rand(n_samples, n_cols)

    def test_basic(self):
        transformers = self.get_transformers()

        sizes = ((10, 6), (10, 3), (10,9), (1, 10))

        for transformer_name, transformer in transformers.items():
            for R, C in sizes:
                with self.subTest(transformer_name=transformer_name, R=R, C=C):
                    t_data = self.generate_sample_data(R, C)
                    data = self.generate_sample_data(R, C)
                    
                    transformer.fit(t_data)

                    for row in data:
                        filtered_row = transformer.transform_sample(row)
                        self.assertIsNotNone(filtered_row)
                        self.assertTrue(len(filtered_row) >0 , "Empty filtered")
                        self.assertFalse(
                            np.any(np.isnan(filtered_row)), "Nans in filtered"
                        )
                        self.assertFalse(
                            np.any(np.isinf(filtered_row)), "Infs in filtered"
                        )
                    transformer.reset()

    
