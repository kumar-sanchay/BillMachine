from collections import defaultdict


class Graph:
    """
    The actual Graph Code using a defaultdict
    """
    def __init__(self, vertices):
        self.dict = defaultdict(list)
        self.v = vertices

    def addEdge(self, src, des, exp):
        n = {'des': des, 'exp': exp}
        self.dict[src].append(n)

    # def get_des(self, src):
    #     n = self.dict[src]
    #     return n.des
    #
    # def get_exp(self, src):
    #     n = self.dict[src]
    #     return


class TopologicalSort:
    """
    Topological sort Algorithm
    """
    def __init__(self, graph:Graph):
        self.graph = graph
        self.visited = [False]*self.graph.v
        self.stack = []

    def topologicalUtil(self, v):
        self.visited[v] = True

        for i in self.graph.dict[v]:
            if not self.visited[i['des']]:
                self.topologicalUtil(i['des'])
        self.stack.insert(0, v)

    def topological_sort(self):
        print(self.graph.dict)
        for i in range(self.graph.v):
            if not self.visited[i]:
                self.topologicalUtil(i)

        return self.stack


if __name__ == '__main__':
    graph = Graph(6)
    graph.addEdge(5, 2, 4)
    graph.addEdge(5, 0, 3)
    graph.addEdge(4, 0, 3)
    graph.addEdge(4, 1, 3)
    graph.addEdge(2, 3, 3)
    graph.addEdge(3, 1, 3)

    t = TopologicalSort(graph)
    print(t.topological_sort())