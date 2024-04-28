class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, key, data=None):
        if key not in self.nodes:
            self.nodes[key] = Node(key, data)

    def add_edge(self, src, dest):
        if src in self.nodes and dest in self.nodes:
            self.nodes[src].add_neighbor(self.nodes[dest])

    def get_node(self, key):
        return self.nodes.get(key, None)

    def remove_node(self, key, data=None):
        node = self.nodes.get(key)
        if node is not None and node.data == data:
            del self.nodes[key]
            for node in self.nodes.values():
                node.remove_neighbor(key)

    def update_node(self, key, data):
        node = self.nodes.get(key)
        if node is not None:
            node.data = data


class Node:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data
        self.neighbors = []
        self.left = None
        self.right = None

    def add_data(self, data):
        if data not in self.data:
            self.data.append(data)

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, key):
        self.neighbors = [neighbor for neighbor in self.neighbors if neighbor.key != key]

    def remove_data(self, data):
        if data in self.data:
            self.data.remove(data)
