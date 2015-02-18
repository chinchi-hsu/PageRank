# PageRank
The implementation of the algorithm PageRank

### Description

The code stems from one of the homework of the course *information retrieval*.

### Running the program

- Compilation
  - gcc -o pagerank -std=c99 -O3 -lm pagerank.c
- Running
  - ./pagerank -d -e -o
  - d: Dumping factor
  - e: Comvergence threshold
  - 0: Path of the output file

### Algorithm

PageRank is implemented using Markov chain. We do not directly compute the eigenvalues since the latter takes more time in practice. (to be honest, the latter is more difficult to implement in C :))

### Data structure

Each graph is constructed using an adjacency list.
