#include <iostream>
#include "ga.h"
#include "individual.h"

using namespace std;

int main(void) {

     //Individual v = Individual("teste");

     //v.print();
     //printf("evaluate = %f\n",v.evaluate());

     // string name, int pop_size = 100, int generations = 100, int elite_size = 10, int tour_size = 20, int mut_rate = 20)

     GA ga_teste = GA("teste", 100, 10, 10, 20, 30);
     ga_teste.envolve();
     
     return(0);
}
