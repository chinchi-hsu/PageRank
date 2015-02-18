# PageRank
The implementation of the algorithm PageRank

### Description

The code stems from one of the homework of the course *information retrieval*.

### Algorithm

PageRank is implemented using Markov chain. We do not directly compute the eigenvalues since the latter takes more time in practice. (to be honest, the latter is more difficult to implement in C :))

### Data structure

Each graph is constructed using an adjacency list.
