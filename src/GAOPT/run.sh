mkdir build
cd build
cmake ../
make

echo "Fibonnaci"
./genetic_algorithm fib

echo "Quicksort"
./genetic_algorithm quicksort

echo "treesort"
./genetic_algorithm treesort

echo "queens"
./genetic_algorithm queens

echo "mm"
./genetic_algorithm mm


