import numpy as np
from rpi_gyro_reader.transformers.column_selector_transformer import ColumnSelectorTransformer
from tests.transformers.itransformer_test import ITransformerTest


class PassTransformerTest(ITransformerTest):

    __test__ = True

    def get_transformers(self):
        return {
            "Base": ColumnSelectorTransformer(),
            "selected": ColumnSelectorTransformer(columns=[0]),
                }

    def test_selection(self):
        selections = ([0],[1],[0,1])
        sizes = ((10, 6),)

        
        for R, C in sizes:
            for  sel_number, selection in enumerate(selections):
                with self.subTest(selection=selection, R=R, C=C):
    
                    t_data = self.generate_sample_data(R, C)
                    data = self.generate_sample_data(R, C)
                    transformer = ColumnSelectorTransformer(columns=selection)
                    
                    transformer.fit(t_data)

                    for row in data:
                        filtered_row = transformer.transform_sample(row)
                        self.assertIsNotNone(filtered_row)
                        self.assertTrue(len(filtered_row) >0 , "Empty filtered")
                        self.assertTrue(len(selection) == len(filtered_row), "Wrong row length")
                        self.assertFalse(
                            np.any(np.isnan(filtered_row)), "Nans in filtered"
                        )
                        self.assertFalse(
                            np.any(np.isinf(filtered_row)), "Infs in filtered"
                        )

    def test_selection_slice(self):
        selections = (slice(None), slice(1), slice(0,2))
        sizes = ((10, 6),)

        
        for R, C in sizes:
            for  sel_number, selection in enumerate(selections):
                with self.subTest(selection=selection, R=R, C=C):
    
                    t_data = self.generate_sample_data(R, C)
                    data = self.generate_sample_data(R, C)
                    transformer = ColumnSelectorTransformer(columns=selection)
                    
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

