# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:51:11 2020

@author: Juan Sebastian Rojas Velandia 
"""

import matplotlib.pyplot as plt
import networkx as nx

class Graph():
    def __init__(self,instance,solution):
        self.instance = instance
        self.solution = solution

    def plot(self):
        
        G = nx.grid_2d_graph(self.instance.ar, self.instance.ac)  # 4x4 grid
        
        # pos = nx.spring_layout(G, iterations=100)
        for i in range(self.instance.ar):
            for j in range(self.instance.ac):
                G.nodes[(i,j)]['cost'] = self.instance.C[i,j]
                G.nodes[(i,j)]['capacity'] = self.instance.Q[i,j]
        pos = dict( (n, n) for n in G.nodes() )
        my_pos = {}
        for key in pos.keys():
            x,y = pos[key]
            my_pos[key] = (y,-x)
        plt.figure()
        plt.plot()
        color=[]
        for i in self.solution.reshape(self.instance.ar*self.instance.ac):
            if i == 1:
                color.append('#a8de99')
            else:
                color.append('#e3aea1')
        label1=nx.get_node_attributes(G,'cost')
        label2=nx.get_node_attributes(G,'capacity')
        labels={}
        for key in label1:
            labels[key]=f'C={label1[key]}\nQ={label2[key]}'
        for i in range(self.instance.ar-1):
            for j in range(self.instance.ac-1):
                G.add_edge((i,j),(i+1,j+1),label=self.instance.R[i,j])
        labeledge=nx.get_edge_attributes(G,'label')
        nx.draw_networkx(G, my_pos, font_size=8,node_color=color,labels=labels)
        nx.draw_networkx_edge_labels(G, my_pos,edge_labels=labeledge)
        
        plt.show()