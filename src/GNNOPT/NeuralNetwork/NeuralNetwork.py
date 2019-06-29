import numpy as np


class NeuralNetwork:
    def __init__(self, iNodes, oNodes, hNodes):
        self.iNodes = iNodes
        self.oNodes = oNodes
        self.hNodes = hNodes
        self.whi = Matrix(self.hNodes, self.iNodes + 1)
        self.whh = Matrix(self.hNodes, self.hNodes + 1)
        self.woh = Matrix(self.oNodes, self.hNodes + 1)

    def output(self, inputsArr):
        inputs = self.whi.singleColumnMatrixFromArray(inputsArr)
        inputsBias = inputs.addBias()
        hiddenInputs = self.whi.dot(inputsBias)
        hiddenOutputs = hiddenInputs.activate(Sigmoid())
        hiddenOutputsBias = hiddenOutputs.addBias()
        hiddenInputs2 = self.whh.dot(hiddenOutputsBias)
        hiddenOutputs2 = hiddenInputs2.activate(Relu())
        hiddenOutputsBias2 = hiddenOutputs2.addBias()
        outputInputs = self.woh.dot(hiddenOutputsBias2)
        outputs = outputInputs.activate(Pass())
        return outputs.toArray()


class Matrix:
    def __init__(self, r, c):
        self.rows = r
        self.cols = c
        self.matrix = np.random.rand(r, c) * (2 / np.sqrt(r))

    def toArray(self):
        array = []
        for r in self.matrix:
            for l in r:
                array.append(l)

        return array

    def dot(self, matrix):
        r = Matrix(self.rows, self.cols)
        r.matrix = self.matrix.dot(matrix.matrix)
        return r

    def addBias(self):
        n = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            n.matrix[i][0] = self.matrix[i][0]
        n.matrix[self.rows][0] = 1
        return n

    def activate(self, func):
        r = Matrix(self.rows, self.cols)
        r.matrix = func.function(self.matrix)
        return r

    def singleColumnMatrixFromArray(self, array):
        n = Matrix(len(array), 1)
        for i in range(len(array)):
            n.matrix[i][0] = array[i]
        return n


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
        return Z

    def function(self, Z):
        return Z
