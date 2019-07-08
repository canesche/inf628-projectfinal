#include <chrono>
#include <cstdio>
#include <cstdlib>


using namespace std;
using namespace std::chrono;

long long int fib(long int long n) {
    if (n <= 2)
        return 1;
    
    return fib(n-1) + fib(n-2);
}

int main(int argc, char * argv[]) {
    
    long long int a = 0; 
    int n = 33;
    if(argc > 1){
      n = atoi(argv[1]);
    }

    double total = 0.0;
    high_resolution_clock::time_point s;
    duration<double> diff = {};
    s = high_resolution_clock::now();
    
    a = fib(n);
	
    diff = high_resolution_clock::now() - s;
    total = diff.count()*1000;
        
    printf("%lf\n",total);
    
   return a;
}
