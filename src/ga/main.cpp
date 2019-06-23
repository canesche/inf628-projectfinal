#include <iostream>
#include "ga.h"
#include "individual.h"

using namespace std;

int main(void) {

     Individual v;

     v.print();
     printf("evaluate = %f\n",v.evaluate());

     return(0);

}
