import heapq
import random
from copy import deepcopy
from math import ceil


class GeneticAlgorithm:
    def __init__(self, num_gen, pop_size, pb_cx, pb_mut, Individual, IndividualArgs, outputfile=None):
        self.num_gen = num_gen
        self.pb_cx = pb_cx
        self.pb_mut = pb_mut
        self.pop_size = pop_size
        self.population = [Individual(IndividualArgs) for _ in range(pop_size)]
        self.outputfile = outputfile
        if outputfile:
            f = open(self.outputfile, 'w')
            f.write('GENERATION,FITNESS MAX,FITNESS MIN,MEAN,STD\n')

    def evolution(self, print_statistics):
        if print_statistics:
            print("Start evolution ...")

        for ind in self.population:
            score = self.evaluate(ind)
            ind.set_fitness(score)

        for g in range(self.num_gen):
            offspring = self.selection(int(ceil(self.pop_size * 0.3)))
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

        if print_statistics:
            print("End of evolution!")
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
        mean = sum(all_fitness_score) / length
        aux = sum(((x - mean) ** 2) for x in all_fitness_score)
        std = ((1 / length) * aux) ** 0.5

        best_ind = max(self.population)
        worst_ind = min(self.population)

        print("Generation %d:" % (generation + 1))
        print(" Evaluated %i individuals" % recal_ind)
        print(" Best individual is: %s" % (best_ind.get_fitness()))
        print(" Worst individual is: %s" % (worst_ind.get_fitness()))
        print(" Fitness Min: %s" % (worst_ind.get_fitness()))
        print(" Fitness Max: %s" % (best_ind.get_fitness()))
        print(" Fitness Avg: %s" % (mean))
        print(" Fitness Std: %s" % (std))
        print()
        if self.outputfile:
            f = open(self.outputfile, 'a')
            f.write(
                '%d, %f, %f, %f, %f\n' % (generation + 1, best_ind.get_fitness(), worst_ind.get_fitness(), mean, std))
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
