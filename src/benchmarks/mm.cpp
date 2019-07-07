#include <chrono>
#include <cstdio>
#include <cstdlib>

using namespace std;
using namespace std::chrono;

int main(int argc, char *argv[]){
    
    int L1 = 100;
    int C1 = 100;

    int L2 = 100;
    int C2 = 100;
    
    int SAMPLES = 10;
    
    if(argc > 4){
        
       L1 = atoi(argv[1]);
       C1 = atoi(argv[2]);
       L2 = atoi(argv[3]);
       C2 = atoi(argv[4]);
       
       if(C1 != L2){
          printf("Error: C1(%d) != L2(%d)\n",C1,L2);    
       }
    }
    
    if(argc > 5){
        SAMPLES = atoi(argv[5]);
    }
    
    auto m1 = new double *[L1];
    auto m2 = new double *[L2];
    auto m3 = new double *[L1];
    
    for(int i = 0; i < L1;i++){
        m1[i] = new double[C1];
        m3[i] = new double[C2];
    }
    
    for(int i = 0; i < L2;i++){
        m2[i] = new double[C2];
    }
    
    high_resolution_clock::time_point tp;
    duration<double> diff = {};
    double cpuExecTime = 0.0;
    
    for(int s = 0; s < SAMPLES; s++){
        tp = high_resolution_clock::now();
        for(int i = 0; i < L1;i++){
            for(int j = 0; j < C2;j++){
                double sum = 0;
                for(int k = 0;k < C1;k++){
                sum += m1[i][k] * m2[k][j];
                }
                m3[i][j] = sum;
            }
        }
        diff = high_resolution_clock::now() - tp;
        cpuExecTime += (diff.count() * 1000);
    }
    
    printf("%f\n",cpuExecTime);
     
    int l = rand()%L1;  
    int c = rand()%C2;    
    double r = m3[l][c];
    
    for(int i = 0; i < L1;i++){
        delete[] m1[i];
        delete[] m3[i];
    }
    
    for(int i = 0; i < L2;i++){
        delete[] m2[i];
    }
    
    delete[] m1;
    delete[] m2;
    delete[] m3;

    
    return r;
}
