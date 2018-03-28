import sys;
import numpy;
from math import sqrt;
from pandas import read_csv;
from scipy.sparse import csr_matrix;
from scipy.stats import spearmanr;
from sklearn.metrics import mean_squared_error;

class Graph:
    def __init__(self):
        self.graph = [];
        self.nodeCount = 0;

    def readFromFile(self, filePath):
        # We assume the node index range [0, N - 1].
        # Each line contains a pair of integers [x, y] representing a directed edge.
        self.graph = read_csv(filePath, header = None, delim_whitespace = True).as_matrix().astype(int);
        self.nodeCount = self.graph.max() + 1;
    
    def runPageRank(self, dampingFactor = 0.85, convergenceThreshold = 1e-8, iterationMax = 1000):
        outdegreeVector = numpy.bincount(self.graph[:, 0], minlength = self.nodeCount);
        
        transitionMatrix = csr_matrix(([1.0 / outdegreeVector[x] for x, y in self.graph], (self.graph[:, 1], self.graph[:, 0])), \
                shape = (self.nodeCount, self.nodeCount));

        sinkNodeVector = numpy.where(outdegreeVector == 0)[0];

        resetVector = numpy.full(self.nodeCount, 1.0 / self.nodeCount);
        self.pagerankVector = numpy.array(resetVector);

        iteration = 1;
        while True: 
            updateVector = dampingFactor * (transitionMatrix.dot(self.pagerankVector) + self.pagerankVector[sinkNodeVector].sum() * resetVector) \
                    + (1.0 - dampingFactor) * resetVector;
    
            error = sqrt(mean_squared_error(updateVector, self.pagerankVector));
            self.pagerankVector = updateVector;
            print("\tIteration", iteration, "\tError", error);
            
            if iteration >= iterationMax or error < convergenceThreshold:
                break; 

            iteration += 1;

    def writePageRankResult(self, filePath):
        numpy.savetxt(filePath, self.pagerankVector[numpy.newaxis].T, fmt = "%.4e");

def main():
    graphFilePath = sys.argv[1];
    pagerankFilePath = sys.argv[2];

    print("Read graph");
    graph = Graph();
    graph.readFromFile(graphFilePath);

    print("Run PageRank");
    graph.runPageRank();
    
    print("Save result");
    graph.writePageRankResult(pagerankFilePath);
    
    print("OK");

if __name__ == "__main__":
    main();
