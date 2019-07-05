from FeaturesExtractor.CodeFeaturesExtractor import CodeFeaturesExtractor
from GeneticAlgorithmGeneric.GeneticAlgorithm import GeneticAlgorithm
from GeneticNeuralNetwork.GeneticNeuralNetwork import MyIndividual
from Utils.Utils import commands_getoutput

code_dir = '../benchmarks/'
work_dir = 'work_dir'

f = CodeFeaturesExtractor()
file = f.get_features(code_dir)[0].get_file_name()
features = f.get_train_data(code_dir)

target = commands_getoutput('llvm-config-8 --host-target')
commands_getoutput('clang++ -w --target=%s -std=c++11 -c -emit-llvm %s -o %s' % (target, file, work_dir + '/out.ll'))

ga = GeneticAlgorithm(100, 10, 0.2, 0.2, MyIndividual, [work_dir, work_dir + '/out.ll', features],
                      work_dir + '/out.csv')
best = ga.evolution(True)
