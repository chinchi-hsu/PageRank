import sys;
import math;

class Graph:
    def __init__(self, nodeCount, dampingFactor, epision):
        self.nodeCount = nodeCount;
        self.dampingFactor = dampingFactor;
        self.epision = epision;
        self.nodeDict = {i: {"outNodes": [], "degree": 0, "currentPageRankScore": 1.0, "newPageRankScore: 0.0"} for i in xrange(1, nodeCount + 1)};

    def addArc(self, nodeID, outNodeID):
        self.nodeDict[nodeID]["outNodes"].append(outNodeID);
        self.nodeDict[nodeID]["degree"] += 1;

    def needHalt(self, allNodes):
        distance = 0.0;
        
        for node in allNodes:
            difference = node.getPageRankScoreDifference();
            distance += difference * difference;

        distance = math.sqrt(distance);

        print "\t\tDistance ", distance;

        return distance < self.epision;

    def runPageRank(self):
        allNodes = self.nodeDict.items();
        
        for (id, node) in allNodes:
            node["currentPageRankScore"] = 1.0;
            node["newPageRankScore"] = 0.0;

        iteration = 1;

        while 1:
            print "\tIteration ", iteration;
    
            print "\tVote scores";
            for (id, node) in allNodes:
                if id % 1000 == 1:
                    print "\t\tNode ", id;

                if node["degree"] == 0:
                    voteScore = node["currentPageRankScore"] / len(allNodes);
                    for (outID, outNode) in allNodes:
                        outNode["newPageRankScore"] += voteScore;
                else:

            print "\tDamp scores";
            for node in allNodes:
                node.dampNewPageRankScore(self.dampingFactor);

            print "\tJudge threshold";
            if self.needHalt(allNodes):
                break;

            print "\tUpdate scores";
            for node in allNodes:
                node.updatePageRankScore();

            iteration += 1;

    def writePageRankScores(self, outputFile):
        for (id, node) in sorted(self.nodeDict.items()):
            outputFile.write(str(id) + ":" + str(node.getPageRankScore()) + "\n");

def main():
    dampingFactor = 0.0;
    epision = 0.0;
    outputName = "";
    inputFileName = "";

    a = 1;

    while 1:
        if a >= len(sys.argv) + 1:
            break;

        if sys.argv[a] == "-d":
            a += 1;
            dampingFactor = float(sys.argv[a]);
        elif sys.argv[a] == "-e":
            a += 1;
            epision = float(sys.argv[a]);
        elif sys.argv[a] == "-o":
            a += 1;
            outputFileName = sys.argv[a];
        else:
            inputFileName = sys.argv[a];
            break;

        a += 1;

    print "d: ", dampingFactor;
    print "e: ", epision;

    print "Read the file and construct the graph";

    inputFile = open(inputFileName, "r");
    nodeCount = int(inputFile.readline().split()[1]);
    graph = Graph(nodeCount, dampingFactor, epision);

    print "Number of nodes: ", nodeCount;

    while 1:
        line = inputFile.readline();
        if not line:
            break;

        outNodeIDs = line.split();
        firstOutNodeIDPair = outNodeIDs[0].split(":");
        nodeID = int(firstOutNodeIDPair[0]);
        firstOutNodeID = int(firstOutNodeIDPair[1]);
        graph.addArc(nodeID, firstOutNodeID);

        for (i, outNodeIDString) in enumerate(outNodeIDs):
            if i == 0:
                continue;

            outNodeID = int(outNodeIDString); 
            graph.addArc(nodeID, outNodeID);
        
    inputFile.close();

    print "Start PageRank";

    graph.runPageRank();

    print "Write results";

    outputFile = open(outputFileName, "w");
    graph.writePageRankScore(outputFile);
    outputFile.close();
    
if __name__ == "__main__":
    main();
