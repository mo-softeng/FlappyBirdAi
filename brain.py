"""
this file is the neural network which is an bipartite directed weighted graph with two layers, first layer consists of 
3 input nodes (i0, i1, i2) which act as the birds vision
and bias node of value 1
second layer is an output node which determines wether the bird flaps (i.e. jumps)
this neural network is known as Perceptron
the edges between the nodes are weighted with values between -1 and 1
the output node generates an output using an activation function
the activation function is a function that will take the sum of the product of the weighted connections and their inputs 
the activation function will then return a value between 0, 1
"""

import node
import connections
import random


class Brain: # perceptron
    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2
        if not clone:
            # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Create bias node
            self.nodes.append(node.Node(3))
            self.nodes[3].layer = 0
            # Create output node
            self.nodes.append(node.Node(4))
            self.nodes[4].layer = 1
            # Create connections
            for i in range(0, 4):
                self.connections.append(connections.Connections(self.nodes[i],
                                                              self.nodes[4],
                                                              random.uniform(-1, 1)))
    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])

    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for j in range(0, self.layers):
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer == j:
                    self.net.append(self.nodes[i])
    
    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].output_value = vision[i]

        self.nodes[3].output_value = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Get output value from output node
        output_value = self.nodes[4].output_value

        # Reset node input values - only node 6 Missing Natural Selection in this case
        for i in range(0, len(self.nodes)):
            self.nodes[i].input_value = 0

        return output_value
    
    def clone(self):
        clone = Brain(self.inputs, True)

        # Clone all the nodes
        for n in self.nodes:
            clone.nodes.append(n.clone())

        # Clone all connections
        for c in self.connections:
            clone.connections.append(c.clone(clone.getNode(c.from_node.id), clone.getNode(c.to_node.id)))

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    # 80 % chance that a connection undergoes mutation
    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()
    