
class Node(object):
    def __init__(self, node_name: str, inlinks: list, outlinks: list):
        self.node_name = node_name
        self.inlinks = inlinks
        self.outlinks = outlinks


class Graph(object):
    def __init__(self):
        self.adj_list = dict()

    def add_node(self, node_name: str, inlinks: list, outlinks: list):
        node = Node(node_name=node_name, inlinks=inlinks, outlinks=outlinks)
        self.adj_list[node_name] = node

    def print_graph(self):
        for node in self.adj_list:
            print(f"{node}:")
            print(f"\tin: {self.adj_list[node].inlinks}")
            print(f"\tout: {self.adj_list[node].outlinks}")


if __name__ == "__main__":
    graph = Graph()
    graph.add_node('A', inlinks=['C'], outlinks=['B', 'C'])
    graph.add_node('B', inlinks=['A', 'C'], outlinks=['D'])
    graph.add_node('C', inlinks=['A', 'B'], outlinks=['A', 'B', 'D'])
    graph.add_node('D', inlinks=['C'], outlinks=['B', 'C'])
    graph.print_graph()
