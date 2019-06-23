#include <iostream>
#include <chrono>

using namespace std;
using namespace chrono;

#define N 5

int f(int n) {
    if (n == 1)
        return 1;
    if (n == 2)
        return 1;
    return f(n-1) + f(n-2);
}

int main() {

    double total = 0;
    for (int i = 0; i < N; i++) {
        auto begin = high_resolution_clock::now();
        int a = f(10);
        duration<double> diff = high_resolution_clock::now() - begin;
        total += diff.count()*1000;
    }

    printf("%f", total/N);
	return 0;
}
