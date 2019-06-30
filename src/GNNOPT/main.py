from FeaturesExtractor.CodeFeaturesExtractor import CodeFeaturesExtractor
from GeneticAlgorithmGeneric.GeneticAlgorithm import GeneticAlgorithm
from GeneticNeuralNetwork.GeneticNeuralNetwork import MyIndividual

dir = '../benchmarks/'
f = CodeFeaturesExtractor()
file = f.get_features(dir)[0].get_file_name()
data = f.get_train_data(dir)
ga = GeneticAlgorithm(100, 100, 0.2, 0.2, MyIndividual, [file, data], 'out.csv')
best = ga.evolution(True)

# import random
# def __crossover(ind1, ind2):
#     l1, c1 = ind1.shape
#     l2, c2 = ind2.shape
#     l, c = min(l1, l2), min(c1, c2)
#     randR = random.randint(1, l - 2)
#     randC = random.randint(1, c - 2)
#     print(randR, randC)
#     for i in range(l):
#         for j in range(c):
#             # if random.random() < 0.5:
#             #    ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]
#             if ((i < randR) or (i == randR and j <= randC)):  # if before the random point then copy from this matric
#                 ind1[i][j], ind2[i][j] = ind2[i][j], ind1[i][j]
#
#
# def __mutate(ind):
#     l, c = ind.shape
#     randC = random.randint(0, c-1)
#     for i in range(l):
#         ind[i][randC] += random.uniform(-1, 1)
#         if ind[i][randC] > 1:
#             ind[i][randC] = 1
#         elif ind[i][randC] < -1:
#             ind[i][randC] = -1
#
#
#
# import numpy as np
#
# a = np.zeros((3, 4)) + 0.1
# b = np.zeros((3, 4))
#
# print(a)
# print()
# print(b)
# print()
# __crossover(a, b)
# print(a)
# print()
# print(b)
# print()
# __mutate(a)
# #__mutate(b)
# print(a)
# print()
# print(b)
