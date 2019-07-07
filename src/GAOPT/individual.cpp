#include "individual.h"
#include <time.h>
#include <vector>
#include <cstring>
#include <fstream>
#include <sys/resource.h>
#include <chrono>

#define NUMBERS_FLAGS 173

using namespace chrono;

// -early-cse-memssa

const char* CONST_FLAGS[NUMBERS_FLAGS] = {
        "-aa", "-adce", "-add-discriminators", "-alignment-from-assumptions","-alloca-hoisting","-always-inline",
        "-argpromotion", "-asan", "-assumption-cache-tracker", "-atomic-expand", "-barrier", "-basicaa", "-basiccg",
        "-bdce", "-block-freq", "-bounds-checking", "-branch-prob", "-break-crit-edges", "-called-value-propagation",
        "-callsite-splitting", "-cfl-anders-aa", "-cfl-steens-aa","-codegenprepare", "-consthoist",
        "-constmerge", "-constprop","-coro-cleanup", "-coro-early", "-coro-elide", "-coro-split", "-correlated-propagation",
        "-cost-model", "-cross-dso-cfi", "-da", "-dce", "-deadargelim", "-delinearize", "-demanded-bits","-die",
        "-div-rem-pairs", "-divergence", "-domfrontier", "-domtree", "-dse", "-dwarfehprepare", "-early-cse", 
        "-ee-instrument", "-elim-avail-extern", "-expand-reductions", "-expandmemcmp",
        "-extract-blocks", "-falkor-hwpf-fix", "-flattencfg", "-float2int", "-forceattrs", "-summary-file -function-import",
        "-functionattrs", "-generic-to-nvvm", "-global-merge", "-globaldce", "-globalopt", "-globals-aa", "-globalsplit",
        "-guard-widening", "-gvn", "-gvn-hoist", "-gvn-sink", "-hotcoldsplit", "-indirectbr-expand", "-indvars",
        "-infer-address-spaces", "-inferattrs", "-inline", "-instcombine", "-instcount","-instnamer", "-instrprof",
        "-instsimplify", "-interleaved-access", "-interleaved-load-combine","-intervals", "-ipconstprop", "-ipsccp",
        "-jump-threading", "-libcalls-shrinkwrap", "-load-store-vectorizer", "-loop-accesses", "-loop-data-prefetch",
        "-loop-deletion", "-loop-distribute", "-loop-extract", "-loop-extract-single", "-loop-guard-widening", "-loop-idiom",
        "-loop-instsimplify", "-loop-interchange", "-loop-load-elim", "-loop-predication", "-loop-reduce", "-loop-reroll",
        "-loop-rotate", "-loop-simplify", "-loop-simplifycfg", "-loop-sink", "-loop-unroll", "-loop-unroll-and-jam",
        "-loop-unswitch", "-loop-vectorize", "-loop-versioning", "-loop-versioning-licm", "-loops", "-lower-expect",
        "-lower-guard-intrinsic", "-loweratomic", "-lowerinvoke", "-lowerswitch", "-lowertypetests", "-make-guards-explicit",
        "-mem2reg", "-memcpyopt", "-memdep", "-memoryssa", "-mergefunc", "-mergeicmps", "-mergereturn", "-mldst-motion",
        "-partial-inliner", "-partially-inline-libcalls", "-print-memderefs", "-reassociate", "-reg2mem", "-regions",
        "-scalarizer", "-sccp", "-simple-loop-unswitch", "-slsr", "-speculative-execution", "-sroa", "-strip", "-strip-nondebug",
        "-tailcallelim", "-bounds-checking-single-trap", "-enable-name-compression", "-enable-load-pre", "-enable-no-infs-fp-math",
        "-enable-no-nans-fp-math", "-enable-no-signed-zeros-fp-math", "-enable-no-trapping-fp-math", "-enable-unsafe-fp-math",
        "-expensive-combines", "-tailcallopt", "-tti", "-tbaa", "-scoped-noalias", "-targetlibinfo", "-verify", "-ee-instrument",
        "-simplifycfg", "-profile-summary-info", "-lazy-branch-prob", "-lazy-block-freq", "-opt-remark-emitter", "-prune-eh",
        "-lazy-value-info", "-pgo-memop-opt", "-lcssa-verification", "-lcssa", "-scalar-evolution", "-licm", "-postdomtree",
        "-rpo-functionattrs", "-slp-vectorizer", "-strip-dead-prototypes"
        };

// Constructor
Individual::Individual(){ }

// Constructor
Individual::Individual(string name){

    this->name = name;

    // Size initial of genes
    srand(time(nullptr)+rand());
    int n;
    const int size = 1; //1+ rand() % 25;
    bool have[NUMBERS_FLAGS];

    for(int i = 0; i < NUMBERS_FLAGS; ++i){
        have[i] = false;
        //if(CONST_FLAGS[i] == "-enable-no-infs-fp-math"){
        //  printf("%d\n", i);
        //}
    }

    // Initializathe elements of genes randomize
    for (int i = 0; i < size; ++i) {
        do {
            n = rand() % NUMBERS_FLAGS;
            if(n == 150 || n == 147 || n == 146 || n == 145 || n == 144 || n == 56 || n == 151 || n == 148 ||
                n == 149 || n == 142 || n == 143){
                if (!have[n]){
                    have[n] = true;
                    break;
                }
            } else {
                break;
            }
        } while (true);

        //printf("%s\n", CONST_FLAGS[46]);

        this->gene.push_back(n);
        //this->gene.push_back(flag_problem[i]);
    }
}

void Individual::setIndividual(vector<int> v, string s) {
    this->gene = v;
    this->name = s;
}

void Individual::change_individual(int i) {
    if (i < get_size_Individual()) {
        srand(time(nullptr) + rand());
        this->gene[i] = rand() % NUMBERS_FLAGS;
    }
}

// get the vector of genes
vector<int> Individual::getIndividual() const {
    return this->gene;
}

int Individual::get_size_Individual() const {
    return this->gene.size();
}

void Individual::print() {
    printf("SIZE: %lu GENE: [", gene.size());
    for (int i = 0; i < gene.size(); ++i) {
        if (gene[i] == NUMBERS_FLAGS-1)
        	printf("<%d>", gene[i]);
        else
        	printf("%d", gene[i]);
        if (i != gene.size()-1)
            printf(" ");
    }
    printf("]\n");
}

// Evaluate the Individual
double Individual::evaluate() const {
    //auto begin = high_resolution_clock::now();
    /*if (this->gene.size() == 0) {
        return -1;
    }*/

    string flags = " ";

    for (int i = 0; i < gene.size(); ++i) {
        flags += CONST_FLAGS[gene[i]];
        flags += " ";
    }

    string create_sys, create_exec;
    string name = this->name;

    // create the optimizer
    create_sys = "opt -no-warn "+flags+" -S -o ../bitecode/opt_"+name+".ll ../bitecode/"+name+".ll\n";
    create_sys += "clang++ -w ../bitecode/opt_"+name+".ll -lm -o "+name+".out";
    create_exec = "./"+name+".out";

    // execute code external
    system(create_sys.c_str());

    duration<double> diff;

    double worst = -1.0, total = 0.0;
    for (int i = 0; i < 10; i++) {
        auto begin = high_resolution_clock::now();
        system(create_exec.c_str());
        diff = high_resolution_clock::now() - begin;
        if (worst < diff.count()) {
            worst = diff.count();
        }
        total += diff.count();
    }

    // time in milliseconds
    return 1.0/(total/10.0);
}

void Individual::saveIndividual(double value){
    ofstream write;
    write.open("../results/best_teste.txt");
    const int tam_gene = get_size_Individual();

    write << tam_gene << "\n";
    write << evaluate()  << "\n";
    for (int i = 0; i < tam_gene; ++i) {
        write << CONST_FLAGS[this->gene[i]] << " ";
    }
    write << "\n";
    write.close();
}

void Individual::setGene(int v) {
    this->gene.push_back(v);
}
