from FeaturesExtractor.CodeFeaturesExtractor import CodeFeaturesExtractor
from GeneticAlgorithmGeneric.GeneticAlgorithm import GeneticAlgorithm
from GeneticNeuralNetwork.GeneticNeuralNetwork import MyIndividual

dir = '../benchmarks/'
f = CodeFeaturesExtractor()
file = f.get_features(dir)[0].get_file_name()
data = f.get_train_data(dir)
ga = GeneticAlgorithm(100, 10, 0.2, 0.2, MyIndividual, [file, data], 'out.csv')
best = ga.evolution(True)
