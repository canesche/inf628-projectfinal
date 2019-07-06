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
            self.weights[f'W{i}'] = np.random.randn(dims[i], dims[i - 1])
            self.weights[f'B{i}'] = np.zeros((dims[i], 1))

    def getError(self):
        return self.J

    def regularizationError(self):
        sum_ = 0.0
        for k in range(1, self.L):
            for i in self.weights[f'W{k}']:
                for j in i:
                    sum_ += (j ** 2.0)

        return (self.lamb / (2 * self.L)) * sum_

    def forward(self, X, Y=None):
        self.cache = {'A1': X}
        for j in range(2, self.L + 1):
            self.cache[f'Z{j}'] = np.dot(self.weights[f'W{j - 1}'], self.cache[f'A{j - 1}']) + self.weights[f'B{j - 1}']
            if j == self.L:
                self.cache[f'A{j}'] = self.output_activation.function(self.cache[f'Z{j}'])
            else:
                self.cache[f'A{j}'] = self.activation.function(self.cache[f'Z{j}'])

        if Y is not None:
            self.J = (-1 / len(Y)) * (
                np.sum(Y * np.log(self.cache[f'A{self.L}']) + (1 - Y) * np.log(1 - self.cache[f'A{self.L}'])))
            self.J += (1 / len(Y)) * self.regularizationError()

        return self.cache[f'A{self.L}']

    def backward(self, Y):
        self.cache[f'd{self.L}'] = self.cache[f'A{self.L}'] - Y
        for j in reversed(range(1, self.L)):
            if j > 1:
                self.cache[f'd{j}'] = np.dot(self.weights[f'W{j}'].T, self.cache[f'd{j + 1}'])
                self.cache[f'd{j}'] = np.multiply(self.cache[f'd{j}'], self.activation.derivative(self.cache[f'Z{j}']))

            self.cache[f'dW{j}'] = (1 / len(Y)) * (
                    (np.dot(self.cache[f'd{j + 1}'], self.cache[f'A{j}'].T)) + self.lamb * self.weights[f'W{j}'])
            self.cache[f'dB{j}'] = (1 / len(Y)) * np.sum(self.cache[f'd{j + 1}'], axis=1, keepdims=True)

    def update(self, alpha):
        for j in range(1, self.L):
            self.weights[f'W{j}'] = self.weights[f'W{j}'] - alpha * self.cache[f'dW{j}']
            self.weights[f'B{j}'] = self.weights[f'B{j}'] - alpha * self.cache[f'dB{j}']

    def train(self, X, Y, alpha, steps):
        for i in range(0, steps):
            self.forward(X, Y)
            self.backward(Y)
            self.update(alpha)
            if i % 5000 == 0:
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
