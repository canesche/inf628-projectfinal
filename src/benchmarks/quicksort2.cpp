#include <chrono>
#include <cstdio>
#include <cstdlib>

using namespace std;
using namespace std::chrono;

void quicksort(double values[], int began, int end)
{
	int i, j, pivo, aux;
	i = began;
	j = end-1;
	pivo = values[(began + end) / 2];
	while(i <= j)
	{
		while(values[i] < pivo && i < end)
		{
			i++;
		}
		while(values[j] > pivo && j > began)
		{
			j--;
		}
		if(i <= j)
		{
			aux = values[i];
			values[i] = values[j];
			values[j] = aux;
			i++;
			j--;
		}
	}
	if(j > began)
		quicksort(values, began, j+1);
	if(i < end)
		quicksort(values, i, end);
}

int main(int argc, char *argv[])
{
  
    int N = 500000;
    
    if(argc > 1){
        
       N = atoi(argv[1]);       
    }
    
    auto array = new double [N];
    
    high_resolution_clock::time_point tp;
    duration<double> diff = {};
    double cpuExecTime = 0.0;

    tp = high_resolution_clock::now();
    
    quicksort(array, 0, N);
    
    diff = high_resolution_clock::now() - tp;
    cpuExecTime = (diff.count() * 1000);
    
    printf("%lf\n",cpuExecTime);
     
    int index = rand()%N;  
    
    double r = array[index];
    
    delete[] array;

    
    return r;
}
