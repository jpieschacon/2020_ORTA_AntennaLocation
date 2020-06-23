# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import networkx as nx


class Graph():
    def __init__(self, instance, solution, sol_q):
        self.instance = instance
        self.solution = solution
        self.sol_q = sol_q

    def plot(self, title):

        G = nx.grid_2d_graph(self.instance.ar, self.instance.ac)  # 4x4 grid

        # pos = nx.spring_layout(G, iterations=100)
        for i in range(self.instance.ar):
            for j in range(self.instance.ac):
                G.nodes[(i, j)]['cost'] = self.instance.C[i, j]
                G.nodes[(i, j)]['capacity'] = self.instance.Q[i, j]
                G.nodes[(i, j)]['usedCapacity'] = self.sol_q[i, j]
        pos = dict((n, n) for n in G.nodes())
        my_pos = {}
        for key in pos.keys():
            x, y = pos[key]
            my_pos[key] = (y, -x)
        plt.figure()
        plt.plot()
        color = []
        for i in self.solution.reshape(self.instance.ar * self.instance.ac):
            if i == 1:
                color.append('#a8de99')
            else:
                color.append('#e3aea1')
        label1 = nx.get_node_attributes(G, 'cost')
        label2 = nx.get_node_attributes(G, 'capacity')
        label3 = nx.get_node_attributes(G, 'usedCapacity')
        labels = {}
        for key in label1:
            labels[key] = f'c={int(label1[key])}\nq={round(label3[key], 3)}\nQ={label2[key]}'
        for i in range(self.instance.ar - 1):
            for j in range(self.instance.ac - 1):
                G.add_edge((i, j), (i + 1, j + 1), label=self.instance.R[i, j])
                G.add_edge((i + 1, j), (i, j + 1))
        labeledge = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx(G, my_pos, font_size=8, node_color=color, labels=labels)
        nx.draw_networkx_edge_labels(G, my_pos, edge_labels=labeledge)
        plt.title(title)
        print(title + ':')
        plt.box(False)
        plt.savefig(f'results/Figures/Instances/instance_{title}.pdf')
        plt.show()
