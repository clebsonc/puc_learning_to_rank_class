from puc_l2r.graph import Graph
import numpy as np


class PageRank(object):
    def __init__(self, graph: Graph):
        self.graph = graph
        self.scores = dict()
        self.__initialize_scores()

    def __initialize_scores(self):
        for node in self.graph.adj_list:
            self.scores[node] = 1/len(self.graph.adj_list)

    def compute(self, iterations=10):
        # initialize scores for all nodes
        new_scores = {x: 0.0 for x in self.graph.adj_list}
        for i in range(iterations):
            for node in self.graph.adj_list:
                inlinks = self.graph.adj_list[node].inlinks
                inlinks_score = np.asarray([self.scores[x] for x in inlinks])
                outlinks_from_inlinks = np.asarray([
                    len(self.graph.adj_list[x].outlinks) for x in inlinks
                ])
                scores_divided = inlinks_score / outlinks_from_inlinks
                new_scores[node] = np.sum(scores_divided)
            self.scores = new_scores.copy()
            print(f"{i}: {self.scores}")
