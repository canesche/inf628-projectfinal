#include <chrono>

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
    
    
    long long int a = f(10);
    
	return a;
}
