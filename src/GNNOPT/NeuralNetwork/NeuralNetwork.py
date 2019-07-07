import numpy as np

class NeuralNetwork:
    def __init__(self, dims, activation_hidden, activation_output, lamb=0):
        self.dims = dims
        self.weights = {}
        self.L = len(dims)
        self.activation = activation_hidden
        self.output_activation = activation_output
        self.lamb = lamb

        for i in range(1, self.L):
            self.weights['W%d' % i] = np.random.randn(dims[i], dims[i - 1]) * (2 / np.sqrt(dims[i - 1]))
            self.weights['B%d' % i] = np.zeros((dims[i], 1))

    def getError(self):
        return self.J

    def regularizationError(self):
        sum_ = 0.0
        for k in range(1, self.L):
            for i in self.weights['W%d' % k]:
                for j in i:
                    sum_ += (j ** 2.0)

        return (self.lamb / (2 * self.L)) * sum_

    def forward(self, X, Y=None):
        self.cache = {'A1': X}
        for j in range(2, self.L + 1):
            self.cache['Z%d' % j] = np.dot(self.weights['W%d' % (j - 1)], self.cache['A%d' % (j - 1)]) + self.weights[
                'B%d' % (j - 1)]
            if j == self.L:
                self.cache['A%d' % j] = self.output_activation.function(self.cache['Z%d' % j])
            else:
                self.cache['A%d' % j] = self.activation.function(self.cache['Z%d' % j])

        if Y is not None:
            self.J = (-1.0 / len(Y)) * (
                np.sum(Y * np.log(self.cache['A%d' % self.L]) + (1.0 - Y) * np.log(1.0 - self.cache['A%d' % self.L])))
            self.J += (1.0 / len(Y)) * self.regularizationError()

        return self.cache['A%d' % self.L]

    def backward(self, Y):
        self.cache['d%d' % self.L] = self.cache['A%d' % self.L] - Y
        for j in reversed(range(1, self.L)):
            if j > 1:
                self.cache['d%d' % j] = np.dot(self.weights['W%d' % j].T, self.cache['d%d' % (j + 1)])
                self.cache['d%d' % j] = np.multiply(self.cache['d%d' % j],
                                                    self.activation.derivative(self.cache['Z%d' % j]))

            self.cache['dW%d' % j] = (1 / len(Y)) * (
                    (np.dot(self.cache['d%d' % (j + 1)], self.cache['A%d' % j].T)) + self.lamb * self.weights[
                'W%d' % j])
            self.cache['dB%d' % j] = (1 / len(Y)) * np.sum(self.cache['d%d' % (j + 1)], axis=1, keepdims=True)

    def update(self, alpha):
        for j in range(1, self.L):
            self.weights['W%d' % j] = self.weights['W%d' % j] - alpha * self.cache['dW%d' % j]
            self.weights['B%d' % j] = self.weights['B%d' % j] - alpha * self.cache['dB%d' % j]

    def train(self, X, Y, alpha, steps, step_print):
        for i in range(0, steps):
            self.forward(X, Y)
            self.backward(Y)
            self.update(alpha)
            if i % step_print == 0:
                print('Error: ', self.J)

    def predict(self, X):
        return self.forward(X) > 0.5

    def plot_decision_boundary(self, X, Y, plt=None):
        x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
        y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
        h = 0.01
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = self.predict(np.c_[xx.ravel(), yy.ravel()].T)
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
        # plt.scatter(X[0, :], X[1, :], c=Y, cmap=plt.cm.Spectral)
        plt.show()

    def plot(self, X, Y, plt):
        plt.scatter(X[0, :], X[1, :], c=Y, s=40, cmap=plt.cm.Spectral)
        plt.show()
