#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

typedef struct{
	int nodeCount;
	int **outNodes;
	int *outDegree;
	double *currentPageRankScore;
	double *newPageRankScore;
	double dampingFactor;
	double epision;
} Graph;

Graph* newGraph(int nodeCount, double dampingFactor, double epision){
	Graph *graph = (Graph*)malloc(sizeof(Graph));

	graph->dampingFactor = dampingFactor;
	graph->epision = epision;

	graph->nodeCount = nodeCount;
	graph->outNodes = (int**)malloc(sizeof(int*) * (nodeCount + 1));
	graph->outDegree = (int*)malloc(sizeof(int) * (nodeCount + 1));
	graph->currentPageRankScore = (double*)malloc(sizeof(double) * (nodeCount + 1));
	graph->newPageRankScore = (double*)malloc(sizeof(double) * (nodeCount + 1));

	for(int v = 1; v <= nodeCount; v ++){
		graph->outNodes[v] = NULL;
		graph->outDegree[v] = 0;
	}

	return graph;
}

void deleteGraph(Graph **graphPointer){
	if(graphPointer == NULL || *graphPointer == NULL){
		return;
	}
	Graph *graph = *graphPointer;
	free(graph->outDegree);
	free(graph->currentPageRankScore);
	free(graph->newPageRankScore);
	
	for(int v = 0; v <= graph->nodeCount; v ++){
		if(graph->outNodes[v] != NULL){
			free(graph->outNodes[v]);
		}
	}

	free(graph->outNodes);

	free(graph);
	*graphPointer = NULL;
}

int scoreNoDifference(double *score1, double *score2, int dimension, double threshold){
	double distance = 0;

	for(int i = 1; i <= dimension; i ++){
		double difference = score1[i] - score2[i];
		distance += difference * difference;
	}
	
	distance = sqrt(distance);
	printf("\t\tDistance %f\n", distance);
	return (distance < threshold) ? 1 : 0;
}

// Runs ths PageRank algorithm on the graph.
// The converged scores of nodes is stored in the variable currentPageRankScore.
void graphRunPageRank(Graph *graph){
	// Initialize the scores.
	for(int v = 1; v <= graph->nodeCount; v ++){
		graph->currentPageRankScore[v] = 1;
		graph->newPageRankScore[v] = 0;
	}

	for(int i = 1; ; i ++){
		printf("\tIteration %d\n", i);

		// Vote the scores to the neighbors of the nodes.
		// Pre-compute the overall score of the zero-out-degree nodes.
		double zeroDegreeScore = 0;

		for(int v = 1; v <= graph->nodeCount; v ++){
			if(graph->outDegree[v] == 0){
				zeroDegreeScore += graph->currentPageRankScore[v];
			}
			else{
				double voteScore = graph->currentPageRankScore[v] / graph->outDegree[v];

				for(int x = 0; x < graph->outDegree[v]; x ++){
					int u = graph->outNodes[v][x];

					graph->newPageRankScore[u] += voteScore;
				}
			}
		}

		zeroDegreeScore /= graph->nodeCount;
		
		// Adjust the scores with the damping factor.
		for(int v = 1; v <= graph->nodeCount; v ++){
			graph->newPageRankScore[v] = (1.0 - graph->dampingFactor) + graph->dampingFactor * (zeroDegreeScore + graph->newPageRankScore[v]);
		}

		// Break the iterations if the scores are converged.
		if(scoreNoDifference(graph->newPageRankScore, graph->currentPageRankScore, graph->nodeCount, graph->epision)){
			break;
		}

		// Update the scores.
		for(int v = 1; v <= graph->nodeCount; v ++){
			graph->currentPageRankScore[v] = graph->newPageRankScore[v];
			graph->newPageRankScore[v] = 0;
		}
	}
}

int main(int argc, char *argv[]){
	double dampingFactor = 0.0;
	double epision = 0.0;
	char inputFileName[100];
	char outputFileName[100];
	
	for(int a = 1; a < argc; a ++){
		if(argv[a][0] == '-'){
			switch(argv[a][1]){
				case 'd':
					a ++;
					sscanf(argv[a], "%lf", &dampingFactor);
					break;
				case 'e':
					a ++;
					sscanf(argv[a], "%lf", &epision);
					break;
				case 'o':
					a ++;
					strcpy(outputFileName, argv[a]);
					break;
			}
		}
		else{
			strcpy(inputFileName, argv[a]);
			break;
		}
	}

	printf("output File %s, input File %s\n", outputFileName, inputFileName);

	printf("Read data\n");
	FILE *inputFile = fopen(inputFileName, "r");
	
	char maxNode[100];
	int nodeCount;
	fscanf(inputFile, "%s%d", maxNode, &nodeCount);
	Graph *graph = newGraph(nodeCount, dampingFactor, epision);
	
	printf("Node count %d, damping factor %f, epision %f\n", nodeCount, dampingFactor, epision);

	int node;
	int outDegree;
	while(fscanf(inputFile, "%d:%d", &node, &outDegree) == 2){
		graph->outDegree[node] = outDegree;
		graph->outNodes[node] = (int*)malloc(sizeof(int) * outDegree);

		for(int u = 0; u < outDegree; u ++){
			fscanf(inputFile, "%d", &graph->outNodes[node][u]);
		}
	}
	
	fclose(inputFile);

	int zeroDegree = 0;
	for(int v = 1; v <= graph->nodeCount; v ++){
		if(graph->outDegree[v] == 0){
			zeroDegree ++;
		}
	}
	printf("Zero-out-degree nodes: %d\n", zeroDegree);

	printf("Run PageRank\n");
	graphRunPageRank(graph);

	printf("Write results\n");
	FILE *outputFile = fopen(outputFileName, "w");
	
	for(int v = 1; v <= graph->nodeCount; v ++){
		fprintf(outputFile, "%d:%f\n", v, graph->currentPageRankScore[v]);
	}

	fclose(outputFile);

	deleteGraph(&graph);
	
	return 0;
}
