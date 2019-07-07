mkdir work_quick work_fib work_floatmm work_tree work_queens

echo "quicksort"
python3 main.py -r run_file -f ../benchmarks/quicksort.cpp -g 100 -i 100 -w work_quick -o quicksort.csv

echo "fib"
python3 main.py -r run_file -f ../benchmarks/fib.cpp -g 100 -i 100 -w work_fib -o fib.csv

echo "treesort"
python3 main.py -r run_file -f ../benchmarks/treesort.cpp -g 100 -i 100 -w work_tree -o treesort.csv

echo "queens"
python3 main.py -r run_file -f ../benchmarks/queens.cpp -g 100 -i 100 -w work_queens -o queens.csv

echo "floatmm"
python3 main.py -r run_file -f ../benchmarks/floatmm.cpp -g 100 -i 100 -w work_floatmm -o floatmm.csv
