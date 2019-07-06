import numpy as np

np.seterr('ignore')

class ActivationFunction:
    def derivative(self, A):
        raise NotImplementedError()

    def function(self, Z):
        raise NotImplementedError()


class Sigmoid(ActivationFunction):
    def derivative(self, Z):
        return np.multiply(self.function(Z), 1 - self.function(Z))

    def function(self, Z):
        return 1 / (1 + np.exp(-Z))


class Relu(ActivationFunction):
    def derivative(self, Z):
        return 1.0 * (Z > 0)

    def function(self, Z):
        return Z * (Z > 0)


class Pass(ActivationFunction):
    def derivative(self, Z):
        return 1

    def function(self, Z):
        return Z
