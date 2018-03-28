# PageRank
The implementation of the algorithm PageRank

** 2018/03/28 update: I implemented a new Python 3 PageRank algorithm that is accelerated by Numpy, Scipy, Scikit-learn and Pandas. I think it as my fatest implementation in pure Python code. **

### Description

The code stems from one of the homework of the course *information retrieval*.

### Running the program

- Compilation
  - gcc -o pagerank -std=c99 -O3 -lm pagerank.c
- Running
  - ./pagerank -d -e -o
  - d: Dumping factor
  - e: Convergence threshold
  - o: Path of the output file

### Algorithm

PageRank is implemented using Markov chain. We do not directly compute the eigenvalues since the latter takes more time in practice. (to be honest, the latter is more difficult to implement in C :))

### Data structure

Each graph is constructed using an adjacency list.
