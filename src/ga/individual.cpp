#include "individual.h"
#include <time.h>
#include <vector>
#include <cstring>
#include <fstream>
#include <sys/resource.h>

#define NUMBERS_FLAGS 51

const char* CONST_FLAGS[NUMBERS_FLAGS] ={
        "-aa", "-adce", "-add-discriminators", "-alignment-from-assumptions","-alloca-hoisting","-always-inline",
        "-argpromotion", "-asan", "-assumption-cache-tracker", "-atomic-expand", "-barrier", "-basicaa", "-basiccg",
        "-bdce", "-block-freq", "-bounds-checking", "-branch-prob", "-break-crit-edges", "-called-value-propagation",
        "-callsite-splitting", "-cfl-anders-aa", "-cfl-steens-aa","-check-debugify","-codegenprepare", "-consthoist",
        "-constmerge", "-constprop","-coro-cleanup", "-coro-early", "-coro-elide", "-coro-split", "-correlated-propagation",
        "-cost-model", "-cross-dso-cfi", "-da", "-dce", "-deadargelim", "-delinearize", "-demanded-bits","-die",
        "-div-rem-pairs", "-divergence", "-domfrontier", "-domtree", "-dse", "-dwarfehprepare", "-early-cse",
        "-early-cse-memssa", "-ee-instrument", "-elim-avail-extern", "-expand-reductions"


        };

// Constructor
Individual::Individual(){
    // Size initial of genes
    srand(time(nullptr)+153);
    int size = 1 + rand() % 50;
    // Initializathe elements of genes randomize
    for (int i = 0; i < size; ++i) {
        this->gene.push_back(rand() % NUMBERS_FLAGS);
    }
}

// Copy Constructor
Individual::Individual(const Individual &other) {
    //this->gene = ;
    for (int i = 0; i < other.gene.size(); i++) {

    }
}

// Destructor
Individual::~Individual() { }

void Individual::setIndividual(vector<int> v) {
    this->gene = v;
}

// get the vector of genes
const vector<int> Individual::getIndividual() {
    return this->gene;
}

void Individual::print() {
    printf("SIZE: %lu GENE: [", gene.size());
    for (int i = 0; i < gene.size(); ++i) {
        printf("%d", gene[i]);
        if (i != gene.size()-1)
            printf(" ");
    }
    printf("]\n");
}

// Evaluate the Individual
const double Individual::evaluate() {
    if (this->gene.size() == 0) {
        return 10000.0;
    }

    char flags[1000] = "";

    for (int i = 0; i < gene.size(); ++i) {
        strcat(flags, CONST_FLAGS[gene[i]]);
        strcat(flags, " ");
    }

    string name = "teste";

    char create_bc[100], create_opt[1000];

    // create a bytecode
    sprintf(create_bc,"clang++ -S -emit-llvm ../benchmarks/%s.cpp -o ../bytecode/%s.ll", name.c_str(), name.c_str());

    // create the optimizer
    sprintf(create_opt,"opt %s -S -o opt.ll ../bytecode/%s.ll", flags, name.c_str()); // opt.ll

    // execute code external
    system(create_bc);
    system(create_opt);
    system("clang++ opt.ll -lm"); // a.out

    system("./a.out > time.txt");

    ifstream read;
    read.open("time.txt", ios::in);

    string time;

    getline(read, time);

    return stod(time);
}

