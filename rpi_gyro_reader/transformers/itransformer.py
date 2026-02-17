import abc
from typing import Any
import numpy as np
class ITransformer(abc.ABC):

    @abc.abstractmethod
    def fit(self, X, y=None)->Any:
        """Fit the filter to the given data."""
        return self

    @abc.abstractmethod
    def transform_sample(self, vec)-> np.typing.NDArray:
        """Update the filter with new IMU data and return filtered values."""
        pass

    @abc.abstractmethod
    def reset(self)->None:
        """Reset the filter to its initial state."""
        pass
