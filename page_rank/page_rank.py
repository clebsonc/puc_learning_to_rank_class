import numpy as np
import operator


class Node(object):
    def __init__(self, node_name, inlinks, outlinks):
        """Build the structure of a node in the web.

        Arguments:
            node_name {string} -- string describing the name of the node
            inlinks {list} -- list of the incoming links to this node
            outlinks {list} -- list of the outgoing links from this node
        """
        self.node_name = node_name
        self.inlinks = inlinks
        self.outlinks = outlinks


class Graph(object):
    def __init__(self):
        self.structure = dict()
        self.graph_size = 0

    def add_node(self, node: Node = None):
        """Add a node to the graph.
        Keyword Arguments:
            node {Node} --The graph Node. (default: {None})
        """
        if node.node_name in self.structure:
            print("Node already exists.")
        else:
            self.structure[node.node_name] = node
            self.graph_size += 1

    def get_node(self, name: str) -> Node:
        """Return the node with the given name.

        Arguments:
            name {str} -- The name of the node to be retrieved from the graph

        Returns:
            Node -- The Node if it exists in the graph.
        """
        if name in self.structure:
            return self.structure.get(name)
        return None

    def print_graph(self):
        """ Print the graph structure """
        for key in self.structure.keys():
            print(key, 'inlink: ', self.structure.get(key).inlinks, 'outlink', self.structure.get(key).outlinks)


class PageRank(object):
    def __init__(self, graph: Graph, number_of_iterations: int = 10):
        """Computes the PageRank for the given graph.

        Arguments:
            graph {Graph} -- The graph to compute the pagerank

        Keyword Arguments:
            number_of_iterations {int} -- Number of iterations required to compute the pagerank (default: {10})
        """
        self.graph = graph
        self.number_of_iterations = number_of_iterations

    def compute(self, alpha=0.85) -> dict:
        """ Compute the page rank for the graph.
        Returns:
            dict -- dictionary of scores for each node in the graph
        """
        scores = dict()
        # get the initial score for each page in the graph
        for key in self.graph.structure:
            scores[key] = 1 / len(self.graph.structure)

        number_of_pages = self.graph.graph_size
        for i in range(self.number_of_iterations):
            print('iteration', i, scores)
            # for every node in the graph, update the current page rank score
            new_score = dict()
            for key, node in self.graph.structure.items():
                # get the score for each incoming link of the current node
                pg_in = np.asarray([scores[x] for x in node.inlinks])
                # get the number of outlinks for all incoming links of the current node.
                out = np.asarray([len(self.graph.structure.get(x).outlinks) for x in node.inlinks])
                new_score[key] = alpha * np.sum(pg_in / out) + (1 - alpha) / number_of_pages
            scores = new_score
        return scores


if __name__ == "__main__":
    graph1 = Graph()
    graph1.add_node(node=Node(node_name='a', outlinks=['b', 'c'], inlinks=['c']))
    graph1.add_node(node=Node(node_name='b', outlinks=['d'], inlinks=['a', 'c']))
    graph1.add_node(node=Node(node_name='c', outlinks=['a', 'b', 'd'], inlinks=['a', 'd']))
    graph1.add_node(node=Node(node_name='d', outlinks=['c'], inlinks=['b', 'c']))

    graph1.print_graph()

    pr = PageRank(graph=graph1, number_of_iterations=100)
    scores = pr.compute()
    print(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))

    print()
    print("Second Graph")
    graph2 = Graph()
    graph2.add_node(node=Node(node_name='a', outlinks=['b', 'd', 'c'], inlinks=['b']))
    graph2.add_node(node=Node(node_name='b', outlinks=['a', 'd'], inlinks=['a', 'd']))
    graph2.add_node(node=Node(node_name='c', outlinks=['d'], inlinks=['a', 'd']))
    graph2.add_node(node=Node(node_name='d', outlinks=['c', 'b'], inlinks=['b', 'c']))

    graph2.print_graph()

    pr = PageRank(graph=graph2, number_of_iterations=30)
    scores = pr.compute()
    print(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))

    print()
    print("Third Graph")
    graph3 = Graph()
    graph3.add_node(node=Node(node_name='1', outlinks=['2', '3', '4', '5', '7'], inlinks=['2', '3', '6']))
    graph3.add_node(node=Node(node_name='2', outlinks=['1'], inlinks=['1', '3', '4']))
    graph3.add_node(node=Node(node_name='3', outlinks=['2', '1'], inlinks=['1', '4', '5']))
    graph3.add_node(node=Node(node_name='4', outlinks=['3', '2', '5'], inlinks=['1', '5']))
    graph3.add_node(node=Node(node_name='5', outlinks=['4', '3', '1', '6'], inlinks=['6', '7', '1', '4']))
    graph3.add_node(node=Node(node_name='6', outlinks=['1', '5'], inlinks=['5']))
    graph3.add_node(node=Node(node_name='7', outlinks=['5'], inlinks=['1']))

    graph3.print_graph()

    pr = PageRank(graph=graph3, number_of_iterations=30)
    scores = pr.compute()
    print(sorted(scores.items(), key=operator.itemgetter(1), reverse=True))
