import heapq
import random
from copy import deepcopy


class GeneticAlgorithm:
    def __init__(self, num_gen, pb_cx, pb_mut, pop_size, Individual,IndividualArgs):
        self.num_gen = num_gen
        self.pb_cx = pb_cx
        self.pb_mut = pb_mut
        self.population = [Individual(IndividualArgs) for _ in range(pop_size)]

    def evolution(self,print_statistics):

        for ind in self.population:
            score = self.evaluate(ind)
            ind.set_fitness(score)

        for g in range(self.num_gen):
            offspring = self.selection(10)
            offspring = list(map(deepcopy, offspring))
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.pb_cx:
                    self.mate(child1, child2)
                    child1.set_fitness(None)
                    child2.set_fitness(None)
            for mutant in offspring:
                if random.random() < self.pb_mut:
                    self.mutate(mutant)
                    mutant.set_fitness(None)

            recal_ind = [ind for ind in offspring if not ind.get_fitness()]

            for ind in recal_ind:
                score = self.evaluate(ind)
                ind.set_fitness(score)

            self.population[:] = offspring

            if print_statistics:
                self.statistics(g, len(recal_ind))

        return max(self.population)

    def getKbest(self, population, k):
        best = heapq.nlargest(k, population)
        return best

    def evaluate(self, ind):
        return ind.evaluate()

    def selection(self, tournsize):
        chosen = []
        n = len(self.population)
        for i in range(n):
            aspirants = [random.choice(self.population) for _ in range(tournsize)]
            chosen.append(max(aspirants))

        return chosen

    def mate(self, ind1, ind2):
        ind1.crossover(ind2)

    def mutate(self, ind):
        ind.mutate()

    def statistics(self, generation, recal_ind):
        all_fitness_score = [ind.get_fitness() for ind in self.population]

        length = len(self.population)
        mean1 = sum(all_fitness_score) / length
        sum2 = sum(x * x for x in all_fitness_score)
        std1 = abs(sum2 / length - mean1 ** 2) ** 0.5

        best_ind = max(self.population)
        worst_ind = min(self.population)

        print("Generation %d:" % (generation + 1))
        print(" Evaluated %i individuals" % recal_ind)
        print(" Best individual is: %s" % (best_ind.get_fitness()))
        print(" Worst individual is: %s" % (worst_ind.get_fitness()))
        print(" Fitness Min: %s" % (worst_ind.get_fitness()))
        print(" Fitness Max: %s" % (best_ind.get_fitness()))
        print(" Fitness Avg: %s" % (mean1))
        print(" Fitness Std: %s" % (std1))
        print()

        f = open('data_graph.txt', 'a')
        f.write('%d,%f\n' % (generation + 1, best_ind.get_fitness()))
        f.close()


class BaseIndividual:
    def __init__(self):
        self.__fitness = 0.0

    def evaluate(self):
        raise NotImplementedError

    def crossover(self, partner):
        raise NotImplementedError

    def mutate(self):
        raise NotImplementedError

    def set_fitness(self, fitness):
        self.__fitness = fitness

    def get_fitness(self):
        return self.__fitness

    def __repr__(self):
        return 'Fitness: %f\n' % self.__fitness

    def __lt__(self, other):
        return self.__fitness < other.get_fitness()

    def __gt__(self, other):
        return self.__fitness > other.get_fitness()

    def __eq__(self, other):
        return self.__fitness == other.get_fitness()