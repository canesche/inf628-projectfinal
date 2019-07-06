import argparse
import pickle
import random
import traceback

from FeaturesExtractor.CodeFeaturesExtractor import CodeFeaturesExtractor
from GeneticAlgorithmGeneric.GeneticAlgorithm import GeneticAlgorithm
from GeneticNeuralNetwork.GeneticNeuralNetwork import NeuralNetworkIndividual
from Utils.Utils import commands_getoutput, map_number


def exec_for_dir(file_dir, work_dir, num_generations, num_individuals, pb_cross, pb_mutate, output_file):
    random.seed(0)

    f = CodeFeaturesExtractor()
    features = f.get_features(file_dir)
    features_train = f.get_train_data(file_dir)
    files = []
    maxi = 0
    for i in range(len(features_train)):
        for j in range(len(features_train[i])):
            if features_train[i][j] > maxi:
                maxi = features_train[i][j]

    for i in range(len(features_train)):
        for j in range(len(features_train[i])):
            features_train[i][j] = map_number(features_train[i][j], 0, maxi, 0, 1)

    for i in range(len(features)):
        commands_getoutput(
            'clang++ -std=c++11 -c -emit-llvm %s -o %s' % (features[i].get_file_name(), work_dir + '/out%d.ll' % i))
        files.append(work_dir + '/out%d.ll' % i)

    ga = GeneticAlgorithm(num_generations, num_individuals, pb_cross, pb_mutate, NeuralNetworkIndividual,
                          [work_dir, files, features_train],
                          work_dir + '/' + output_file)
    best = ga.evolution(True)

    pickle_out = open(work_dir + '/best.dat', 'wb')
    pickle.dump(best, pickle_out)
    pickle_out.close()


def exec_for_file(file_path, work_dir, num_generations, num_individuals, pb_cross, pb_mutate, output_file):
    random.seed(0)

    f = CodeFeaturesExtractor()
    features_train = f.get_single_train_data(file_path)

    maxi = 0
    for i in range(len(features_train)):
        for j in range(len(features_train[i])):
            if features_train[i][j] > maxi:
                maxi = features_train[i][j]

    for i in range(len(features_train)):
        for j in range(len(features_train[i])):
            features_train[i][j] = map_number(features_train[i][j], 0, maxi, 0, 1)

    commands_getoutput('clang++ -std=c++11 -c -emit-llvm %s -o %s' % (file_path, work_dir + '/out.ll'))

    ga = GeneticAlgorithm(num_generations, num_individuals, pb_cross, pb_mutate, NeuralNetworkIndividual,
                          [work_dir, [work_dir + '/out.ll'], features_train],
                          work_dir + '/' + output_file)
    best = ga.evolution(True)

    pickle_out = open(work_dir + '/best.dat', 'wb')
    pickle.dump(best, pickle_out)
    pickle_out.close()


def get_args():
    ap = argparse.ArgumentParser('python3 main.py')
    ap.add_argument('-r', '--run', required=True,
                    help='\'test\': Run best individual for one input file.\n'
                         '\'flags\': Show set of flags of the best individual.\n'
                         '\'run_file\': Run genetic algorithm for input file.\n'
                         '\'run_dir\': Run genetic algorithm for all files in directory.')

    ap.add_argument('-f', '--file', help='Input file C/C++')
    ap.add_argument('-d', '--dir', help='Location for input C/C++ files')

    ap.add_argument('-g', '--generations', help='Number of generations: default 100', default=100)
    ap.add_argument('-i', '--individuals', help='Number of individuals: default 100', default=100)
    ap.add_argument('-c', '--cross_prob', help='Probability of two individuals performing the crossing: default 0.2',
                    default=0.2)
    ap.add_argument('-m', '--mut_prob', help='Probability of an individual being mutated: default 0.2', default=0.2)
    ap.add_argument('-o', '--output', help='Output file for statistics', required=True)
    ap.add_argument('-w', '--work_dir', help='Directory for storing auxiliary files', required=True)

    return ap


if __name__ == "__main__":
    ap = get_args()
    args = vars(ap.parse_args())
    num_generations = int(args['generations'])
    num_individuals = int(args['individuals'])
    pb_cross = float(args['cross_prob'])
    pb_mutate = float(args['mut_prob'])
    work_dir = args['work_dir']
    file_dir = args['dir']
    file_path = args['file']
    output_file = args['output']

    if args['run'] == 'flags' and file_path:
        try:
            f = open(work_dir + '/best.dat', 'rb')
            ind = pickle.load(f)
            f.close()
            f = CodeFeaturesExtractor()
            features_train = f.get_single_train_data(file_path)
            maxi = 0
            for i in range(len(features_train)):
                for j in range(len(features_train[i])):
                    if features_train[i][j] > maxi:
                        maxi = features_train[i][j]

            for i in range(len(features_train)):
                for j in range(len(features_train[i])):
                    features_train[i][j] = map_number(features_train[i][j], 0, maxi, 0, 1)

            commands_getoutput(
                'clang++ -std=c++11 -c -emit-llvm %s -o %s' % (file_path, work_dir + '/out.ll'))
            print('Flags: %s' % ind.get_flags()[0])

        except Exception as e:
            traceback.print_exc()
            exit(1)
    elif args['run'] == 'test' and file_path:
        try:
            f = open(work_dir + '/best.dat', 'rb')
            ind = pickle.load(f)
            f.close()
            f = CodeFeaturesExtractor()
            features_train = f.get_single_train_data(file_path)
            maxi = 0
            for i in range(len(features_train)):
                for j in range(len(features_train[i])):
                    if features_train[i][j] > maxi:
                        maxi = features_train[i][j]

            for i in range(len(features_train)):
                for j in range(len(features_train[i])):
                    features_train[i][j] = map_number(features_train[i][j], 0, maxi, 0, 1)

            commands_getoutput(
                'clang++ -std=c++11 -c -emit-llvm %s -o %s' % (file_path, work_dir + '/out.ll'))
            print('Execution time: %f' % ind.evaluate())

        except Exception as e:
            print(e)
            traceback.print_exc()
    elif args['run'] == 'run_file' and file_path:
        try:
            exec_for_file(file_path, work_dir, num_generations, num_individuals, pb_cross, pb_mutate, output_file)
        except Exception as e:
            print(e)
            traceback.print_exc()
    elif args['run'] == 'run_dir':
        try:
            exec_for_dir(file_dir, work_dir, num_generations, num_individuals, pb_cross, pb_mutate, output_file)
        except Exception as e:
            traceback.print_exc()
            exit(4)
    elif not file_path and args['run'] != 'run_file':
        print('File path missing!')
    else:
        ap.print_help()
