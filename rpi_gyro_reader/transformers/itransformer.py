import abc

class ITransformer(abc.ABC):

    @abc.abstractmethod
    def transform_sample(self, vec) -> tuple[float, float, float, float, float, float]:
        """Update the filter with new IMU data and return filtered values."""
        pass

    @abc.abstractmethod
    def reset(self):
        """Reset the filter to its initial state."""
        pass
