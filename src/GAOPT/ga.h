#ifndef GA_H
#define GA_H

#include "individual.h"

class GA {
    private:
        string name;
        int population_size;
        int generations_size;
        int elite_size;
        int tournament_size;
        int reward;
        int mutation_rate;
        vector<pair<double, Individual>> population;
    public:
        GA(string, int, int, int, int, int);
        int get_size_population() const;
        int get_size_elite() const;
        int get_size_generations() const;
        int get_size_tournament() const;
        int get_mutate_rate() const;
        Individual tournament(vector<pair<double, Individual>> , int);
        pair<Individual,Individual> crossover(Individual , Individual);
        pair<double, Individual> mutation(pair<double, Individual> );
        void print(int);
        void envolve();


};

#endif