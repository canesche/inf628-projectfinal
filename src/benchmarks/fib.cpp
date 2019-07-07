#include <chrono>
#include <cstdio>

using namespace std;
using namespace std::chrono;

long long int f(long n) {
    if (n == 1)
        return 1;
    if (n == 2)
        return 1;
    return f(n-1) + f(n-2);
}

int main() {
    
    long long int a; 
    
    double total = 0.0;
    high_resolution_clock::time_point s;
    duration<double> diff = {};
    
    for (int i = 0; i < 10; ++i) {
    	s = high_resolution_clock::now();
		a = f(33);
		diff = high_resolution_clock::now() - s;
		total += diff.count()*1000;
    }
    
    printf("%f\n",total/10);
    
	return 0;
}
