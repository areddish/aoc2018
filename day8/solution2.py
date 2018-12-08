import collections

TEST = ("test.txt",)
INPUT = ("input.txt",)

WHICH = INPUT

class Node:
    def __init__(self, id):
        self.name = chr(id+65)
        self.children = []
        self.metadata = []

    def add_child(self, node):
        self.children.append(node)

    def add_metadata(self, md):
        self.metadata.append(md)

    def get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        value = 0
        for x in self.metadata:
            # 1-based -> 0-based
            index = x - 1
            if (index >=0 and index < len(self.children)):
                value += self.children[index].get_value()

        #print(self.name, value)
        return value

def read_node(nodes, input_set):
    node_index = len(nodes)
    node = Node(node_index)
    nodes[node_index] = node
    
    num_child_nodes = input_set.pop()
    num_metadata_entries = input_set.pop()

    #print (node.name,"has",num_child_nodes,"and",num_metadata_entries)

    for x in range(num_child_nodes):
        node.add_child(read_node(nodes, input_set))

    for x in range(num_metadata_entries):
        node.add_metadata(input_set.pop())

    return node

with open(WHICH[0], "rt") as file:
    data = file.readline().strip()

    input_set = [int(x) for x in data.split(' ')]
    input_set.reverse()
    #print (input_set)

    nodes = collections.defaultdict(list)
    root = read_node(nodes, input_set)

    print ("Part 1", "-"*50)
    running_sum = 0
    for x in nodes:
        running_sum += sum(nodes[x].metadata)
    print(running_sum)

    print ("Part 2", "-"*50)
    print (root.get_value())