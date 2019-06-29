#include <iostream>
#include "ga.h"
#include "individual.h"

using namespace std;

int main(void) {

     //Individual v;

     //v.print();
     //printf("evaluate = %f\n",v.evaluate());

     GA ga = GA("teste", 100, 100, 10, 20, 20);

     ga.envolve();

     ga.print(0);
     ga.print(1);
     ga.print(2);
     ga.print(3);
     ga.print(4);

     return(0);

}
