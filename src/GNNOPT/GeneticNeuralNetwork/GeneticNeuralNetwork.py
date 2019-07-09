import random

from GeneticAlgorithmGeneric.GeneticAlgorithm import BaseIndividual
from NeuralNetwork.ActivationFunctions import Relu, Sigmoid
from NeuralNetwork.NeuralNetwork import NeuralNetwork
from Utils.Utils import map_number, commands_getoutput, command_shell


class NeuralNetworkIndividual(BaseIndividual):
    def __init__(self, args):
        super().__init__()
        self.work_dir = args[0]
        self.ll_file = args[1]
        self.features = args[2]
        self.flags = args[3]
        self.bc_file = '%s/out.bc' % self.work_dir
        self.exe_file = '%s/out.exe' % self.work_dir
        self.max_flags = len(self.flags)

        num_hidden = random.randint(1, 5)
        dims = [random.randint(10, 30) for _ in range(num_hidden + 2)]
        dims[0] = len(self.features)
        dims[num_hidden + 1] = random.randint(10, self.max_flags - 1)

        self.gene = NeuralNetwork(dims, Relu(), Sigmoid(), 0.0)

    def get_flags(self):
        r = ''
        flags = []
        out = self.gene.forward(self.features).T
        for line in out:
            for col in line:
                x = int(map_number(col, 0, 1, 0, len(self.flags) - 1))
                if x < 0:
                    x = 0
                elif x >= self.max_flags:
                    x = self.max_flags - 1

                r += self.flags[x] + ' '
            flags.append(r)
            r = ''
        return flags

    def evaluate(self):
        t = 0
        for flags, ll_file in zip(self.get_flags(), self.ll_file):
            if command_shell('opt %s %s -o %s > /dev/null' % (flags, ll_file, self.bc_file)):
                if command_shell('clang++ -w %s -o %s > /dev/null' % (self.bc_file, self.exe_file)):
                    r = commands_getoutput(self.work_dir + '/measurer.sh %s 3' % self.exe_file)
                    t = float(r)
                else:
                    t = 1000000
            else:
                t = 100000
        return 1 / t

    def __crossover(self, ind1, ind2):
        l1, c1 = ind1.shape
        l2, c2 = ind2.shape
        l, c = min(l1, l2), min(c1, c2)
        randR = random.randint(0, l - 1)
        randC = random.randint(0, c - 1)
        for i in range(l):
            for j in range(c):
                if (i < randR) or (i == randR and j <= randC):
                    ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]

    def __ucrossover(self, ind1, ind2, prob_m):
        l1, c1 = ind1.shape
        l2, c2 = ind2.shape
        l, c = min(l1, l2), min(c1, c2)
        for i in range(l):
            for j in range(c):
                if random.random() < prob_m:
                    ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]

    def crossover(self, partner):
        for w, pw in zip(self.gene.weights, partner.gene.weights):
            # self.__ucrossover(self.gene.weights[w], partner.gene.weights[pw], 0.3)
            self.__crossover(self.gene.weights[w], partner.gene.weights[pw])

    def __mutate(self, ind):
        l, c = ind.shape
        randC = random.randint(0, l - 1)
        for i in range(c):
            ind[randC][i] += 0.1 * (random.random() * 2 - 1)

    def __umutate(self, ind, prob_m):
        l, c = ind.shape
        for i in range(l):
            for j in range(c):
                if random.random() < prob_m:
                    ind[i][j] += 0.1 * (random.random() * 2 - 1)

    def mutate(self):
        for w in self.gene.weights:
            self.__mutate(self.gene.weights[w])
            # self.__umutate(self.gene.weights[w], 0.01)
