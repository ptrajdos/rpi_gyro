import abc

class ITransformer(abc.ABC):

    @abc.abstractmethod
    def fit(self, X):
        """Fit the filter to the given data."""
        return self

    @abc.abstractmethod
    def transform_sample(self, vec):
        """Update the filter with new IMU data and return filtered values."""
        pass

    @abc.abstractmethod
    def reset(self):
        """Reset the filter to its initial state."""
        pass
