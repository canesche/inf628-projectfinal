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
        void setIndividual(vector<int>);
        const int get_size_Individual();
        const vector<int> getIndividual();
        void change_individual(int i);
        const double evaluate();
        void print();
        void saveIndividual();
};

#endif