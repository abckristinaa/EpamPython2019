"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной
Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)
"""


class Graph:
    def __init__(self, E):
        self.E = E
        self.index = -1
        self.visited = []

    def bfs(self):
        queue = []
        for node in self.E:
            queue.append(node)
            while queue:
                node = queue.pop(0)
                if node not in self.visited:
                    self.visited.append(node)
                    queue.extend(self.E[node])
        return self.visited

    def __iter__(self):
        self.bfs()
        return self

    def __next__(self):
        if self.index == len(self.visited) - 1:
            self.visited = []
            raise StopIteration
        self.index += 1
        return self.visited[self.index]


E = {'A': ['B', 'C', 'D'],
     'B': ['C'],
     'C': [],
     'D': ['A']}

graph = Graph(E)
for vertex in graph:
    print(vertex)
