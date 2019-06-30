import random

from GeneticAlgorithmGeneric.GeneticAlgorithm import BaseIndividual, GeneticAlgorithm


class MyIndividual(BaseIndividual):
    def __init__(self, args):
        super().__init__()
        self.gene = [0 for _ in range(10)]

    def evaluate(self):
        return sum(self.gene)

    def crossover(self, partner):
        size = min(len(self.gene), len(partner.gene))
        cxpoint = random.randint(1, size - 1)
        self.gene[cxpoint:], partner.gene[cxpoint:] = partner.gene[cxpoint:], self.gene[cxpoint:]

    def mutate(self):
        for i in range(len(self.gene)):
            if random.random() < 0.1:
                self.gene[i] = 1 if self.gene[i] == 0 else 0


ga = GeneticAlgorithm(100, 100, 0.2, 0.2, MyIndividual, None, None)
ga.evolution(True)
