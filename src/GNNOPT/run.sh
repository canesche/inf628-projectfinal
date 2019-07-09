mkdir work_dir

echo "quicksort"
python3 main.py -r run_file -f ../benchmarks/quicksort.cpp -b best_quicksort.dat -g 100 -i 100 -w work_dir -o quicksort.csv

echo "fib"
python3 main.py -r run_file -f ../benchmarks/fib.cpp -b best_fib.dat -g 100 -i 100 -w work_dir -o fib.csv

echo "treesort"
python3 main.py -r run_file -f ../benchmarks/treesort.cpp -b best_treesort.dat -g 100 -i 100 -w work_dir -o treesort.csv

echo "queens"
python3 main.py -r run_file -f ../benchmarks/queens.cpp -b best_queens.dat -g 100 -i 100 -w work_dir -o queens.csv

echo "mm"
python3 main.py -r run_file -f ../benchmarks/mm.cpp -b best_mm.dat -g 100 -i 100 -w work_dir -o mm.csv
