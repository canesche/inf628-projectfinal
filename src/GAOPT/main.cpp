#include <iostream>
#include "ga.h"
#include "individual.h"

using namespace std;

int main(int argc, char* argv[]) {

    if(argc < 2) {
        printf("Number of arguments invalids!\n");
        printf("Please, pass the name of algorithm\n");
        return 0;
    }

    string name = argv[1];

     // name, pop_size, generation, elite_size, tour_size, mut_rate, grow_rate
     GA ga_fib = GA(name, 100, 100, 10, 20, 20, 30);
     ga_fib.envolve();

     return(0);
}
