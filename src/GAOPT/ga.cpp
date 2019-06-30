#include <algorithm>
#include <cmath>
#include "ga.h"
#include "individual.h"

GA::GA(string name, int pop_size = 100, int generations = 100, int elite_size = 10, int tour_size = 20, int mut_rate = 20) {
    srand(time(nullptr)+rand());
    this->name = name;
    this->population_size = pop_size;
    this->generations_size = generations;
    this->elite_size = elite_size;
    this->tournament_size = tour_size;
    this->mutation_rate = mut_rate;

    // create a bitecode
    string create_bc = "clang++-8 -S -emit-llvm ../../benchmarks/"+name+".cpp -o ../bitecode/"+name+".ll";
    system(create_bc.c_str());

    for (int i = 0; i < pop_size; ++i) {
        Individual v = Individual(name);
        population.push_back(make_pair(v.evaluate(), v));
    }
}

int GA::get_size_population() const {
    return this->population_size;
}

int GA::get_size_elite() const {
    return this->elite_size;
}

int GA::get_size_generations() const {
    return this->generations_size;
}

void GA::print(int number) {
    printf("Reward: %f\n", this->population[number].first);
    this->population[number].second.print();
}

int GA::get_mutate_rate() const {
    return this->mutation_rate;
}

int GA::get_size_tournament() const {
    return this->tournament_size;
}

bool compareInterval(pair<double,Individual> i1, pair<double,Individual> i2) {
    return (i1.first > i2.first);
}

pair<double, Individual> GA::mutation(pair<double, Individual> ind){
    srand(time(nullptr)+rand());
    int prob;
    for (int i = 0; i < ind.second.get_size_Individual(); ++i) {
        prob = 1 + rand() % 100;
        if (prob <= get_mutate_rate()){
            ind.second.change_individual(i);
        }
    }

    // probability of grow up the vector
    prob = 1 + rand() % 100;
    if (prob <= get_mutate_rate()){
        int n = 1 + rand() % 10;
        for (int i = 0; i < n; ++i) {
            ind.second.setGene(rand() % 173);
        }
    }

    return make_pair(ind.second.evaluate(), ind.second);
}

Individual GA::tournament(vector<pair<double, Individual>> pop, int tam_population) {
    Individual best_ind = pop[rand()%get_size_population()].second;
    double best_ind_reward = best_ind.evaluate();

    int tam_tounament = get_size_tournament();
    vector<int> participants(tam_tounament);

    // create vector of participants
    for (int i = 0; i < tam_tounament; ++i) {
        participants[i] = rand() % tam_population;
    }

    for(int i = 0; i < tam_tounament; ++i) {
        if (best_ind_reward < pop[participants[i]].first) {
            best_ind_reward = pop[participants[i]].first;
            best_ind = pop[participants[i]].second;
        }
    }

    return best_ind;
}

pair<Individual,Individual> GA::crossover(Individual i1, Individual i2) {

    int n1 = rand() % i1.get_size_Individual();
    int n2 = rand() % i2.get_size_Individual();

    Individual f1, f2;
    vector<int> aux1(n1+(i2.get_size_Individual()-n2));
    vector<int> aux2(n2+(i1.get_size_Individual()-n1));

    int i;
    // filho 1
    for (i = 0; i < n1; ++i) {
        aux1[i] = i1.getIndividual()[i];
    }
    for (i = n1; i < n1+i2.get_size_Individual()-n2; ++i) {
        aux1[i] = i2.getIndividual()[i-n1];
    }

    // filho 2
    for (i = 0; i < n2; ++i) {
        aux2[i] = i2.getIndividual()[i];
    }
    for (i = n2; i < n2+i1.get_size_Individual()-n1; ++i) {
        aux2[i] = i1.getIndividual()[i-n2];
    }

    f1.setIndividual(aux1, this->name);
    f2.setIndividual(aux2, this->name);

    return make_pair(f1, f2);
}

void GA::envolve() {

    int tam_generation = get_size_generations();
    int tam_elite = get_size_elite();
    int tam_population = get_size_population();

    vector<pair<double, Individual>> new_pop(tam_population);
    pair<Individual,Individual> child;
    pair<double,Individual> best_pop_global;

    best_pop_global.first = population[0].first;
    best_pop_global.second = population[0].second;
    int id_best = 0; 

    for (int i = 0; i < tam_generation; ++i) {
        // sorting vector population
        sort(population.begin(), population.end(), compareInterval);

        printf("Generation: %d best individual %f\n", i, population[0].first);
        population[0].second.print();

        if (best_pop_global.first < population[0].first) {
            best_pop_global.first = population[0].first;
            best_pop_global.second = population[0].second;
            id_best = i;
        }

        if (i == tam_generation-1) {
            printf("Best all Generation: %d best individual %f\n", id_best, best_pop_global.first);
            best_pop_global.second.print();

            // save the file in txt
            best_pop_global.second.saveIndividual(best_pop_global.first);

            break;
        }

        // selection the best individuals of population before
        for (int j = 0; j < tam_elite; ++j) {
            new_pop[j] = mutation(population[i]);
        }

        Individual c1, c2;

        for (int j = tam_elite; j < tam_population; j+=2) {
            c1 = tournament(population, tam_population);
            c2 = tournament(population, tam_population);

            child = crossover(c1, c2);

            new_pop[j] = make_pair(child.first.evaluate(), child.first);
            new_pop[j+1] = make_pair(child.second.evaluate(), child.second);
        }

        // update the population
        population = new_pop;
    }
}
