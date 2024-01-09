import sys
from pathlib import Path
import os
sys.path.append(str(Path(__file__).resolve().parents[1]))
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum



#to change the values of the graphe you can use enum value method 
class CustomSettings(Enum):
    with_labels = True
    node_size = 600
    node_color = "red"
    font_color = "orange"
    font_size = 5
    font_family = 'sans-serif'
    font_weight = 'bold'
    edge_weight_coif= 2




class SocialGraph:
    def __init__(self,num_students) -> None:
        self.num_students=num_students
        self.friendshipMatrix =self.matrice_initialisation()
        self.G = None  # creation of the friendship matrix initialised by 0
        
    def matrice_initialisation(self)  :
        matrix=[[0]*self.num_students for _ in range(self.num_students)]
        # for i in range(self.num_students):
        #    matrix[i][i] = 1
        return   matrix
              
    def establishFriendshipBetween(self, user1Id: int, user2Id: int, coeff: float=.1 ):
        if user1Id <= self.num_students and user2Id <= self.num_students :
            self.friendshipMatrix[user1Id][user2Id]=coeff
            self.friendshipMatrix[user2Id][user1Id]=coeff 
        
            
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id][user2Id]
            
    ####graphics
    def render(self, users: list, currentUserId):
        colors = []
        labels = {}
        matrix = np.array(self.friendshipMatrix)
        for usr in users:
            labels[usr.id] = usr.username
            if usr.id == currentUserId:
                colors.append("blue")
            elif users[currentUserId].isFriendOf(usr, self):
                colors.append("yellow")
            else:
                colors.append("grey")
        self.G = nx.from_numpy_array(matrix, create_using=nx.Graph)
        pos = nx.circular_layout(self.G)
        plt.figure(figsize=(20,10))
        # nx.draw(self.G, pos = pos, with_labels = True, node_color = colors, labels = labels, font_color = "black", font_size = 20)
        
        edge_labels = {(i, j): matrix[i, j] for i, j in zip(*matrix.nonzero()) if i < j}
        edge_widths = [3*matrix[i, j] for i, j in zip(*matrix.nonzero()) if i < j]

        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=edge_labels, font_color="black", font_size = 14)
        nx.draw(self.G, pos=pos, with_labels=True, node_color=colors, labels=labels, font_color="black", width=edge_widths, edge_color='black', font_size=14, node_size = 2000)

        
        legend_labels = {
            "blue": "Utilisateur Actuel",
            "yellow": "Amis",
            "grey": "Non-Amis"
        }
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                           for color, label in legend_labels.items()]
        plt.legend(handles=legend_elements, loc='upper right')

    def show(self):
        plt.show()

    def save(self, filename):
        plt.savefig(filename)
        
