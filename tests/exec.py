from Utils.Utils import commands_getoutput, map_number
import os
import time

work_dir =  '../src/benchmarks'

GOPT_FLAGS = ''
GNNOPT_FALGS = ''

arq = open('results_time.csv', 'w')
arq.write("algorithm,clang O0, clang O1, clang O2, clang O3, clang Os, gcc O0, gcc O1, gcc O2, gcc O3, gcc Os, GAOPT, GNNOPT\n")

for _, _, archives in os.walk('../src/benchmarks'):
    for name in archives:
        if name[-4:] == ".cpp":
            print(name)

            arq.write(name[:-4]+",")

            commands_getoutput('mkdir %s' %name[:-4])

            for i in range(0, 4):
                commands_getoutput('clang++ -O'+str(i)+' -o '+name[:-4]+'/clang_O'+str(i)+'_'+name[:-4]+'.out ../src/benchmarks/'+name)
                commands_getoutput('g++ -O'+str(i)+' -o '+name[:-4]+'/gcc_O'+str(i)+'_'+name[:-4]+'.out ../src/benchmarks/'+name)
            commands_getoutput('clang++ -Os -o '+name[:-4]+'/clang_Os_'+name[:-4]+'.out ../src/benchmarks/'+name)
            commands_getoutput('g++ -Os -o '+name[:-4]+'/gcc_Os_'+name[:-4]+'.out ../src/benchmarks/'+name)

            #clang
            for i in range(0, 4):
                total = 0
                for j in range(0, 10):
                    begin = time.time()
                    commands_getoutput('./'+name[:-4]+'/clang_O0_'+name[:-4]+'.out')
                    end = time.time()
                    total += end-begin
                total = total / 10
                arq.write(str(total)+",")
            for j in range(0, 10):
                begin = time.time()
                commands_getoutput('./'+name[:-4]+'/clang_Os_'+name[:-4]+'.out')
                end = time.time()
                total += end-begin
            arq.write(str(total)+",")
            # gcc
            for i in range(0, 4):
                total = 0
                for j in range(0, 10):
                    begin = time.time()
                    commands_getoutput('./'+name[:-4]+'/gcc_O0_'+name[:-4]+'.out')
                    end = time.time()
                    total += end-begin
                total = total / 10
                arq.write(str(total)+",")
            for j in range(0, 10):
                begin = time.time()
                commands_getoutput('./'+name[:-4]+'/gcc_Os_'+name[:-4]+'.out')
                end = time.time()
                total += end-begin
            arq.write(str(total)+"\n")

            
            
            
            
