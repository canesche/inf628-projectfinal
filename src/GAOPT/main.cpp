#include <iostream>
#include "ga.h"
#include "individual.h"

using namespace std;

int main(void) {

     // name, pop_size, generation, elite_size, tour_size, mut_rate, grow_rate
     GA ga_fib = GA("fib", 100, 100, 10, 20, 20, 30);
     ga_fib.envolve();

    //GA ga_quick = GA("quicksort", 10, 10, 10, 20, 20, 30);
    //ga_quick.envolve();

     return(0);
}
