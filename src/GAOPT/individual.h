#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H

#include <string>
#include <vector>

using namespace std;

class Individual {
    private:
        vector<int> gene;
        string name;

    public:
        Individual();
        Individual(string);
        void setIndividual(vector<int> , string );
        int get_size_Individual() const;
        vector<int> getIndividual() const;
        void change_individual(int );
        double evaluate() const;
        void print();
        void saveIndividual(double );
        void setGene(int );
};

#endif