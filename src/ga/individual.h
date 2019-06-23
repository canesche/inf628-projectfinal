#ifndef INDIVIDUAL_H
#define INDIVIDUAL_H

#include <string>
#include <vector>

using namespace std;

class Individual {
    private:
        vector<int> gene;

    public:
        Individual();
        Individual(const Individual &);
        ~Individual();
        void setIndividual(vector<int>);
        const vector<int> getIndividual();
        const double evaluate();
        void print();
        void saveIndividual();
};

#endif