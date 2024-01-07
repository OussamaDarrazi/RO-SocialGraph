import sys
from pathlib import Path
import os
import numpy as np
# Add the directory containing 'database' to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Now you can import from 'database'
from database.date_base_etudiant_iagi import DATA_LISTE_IAGI

# Use 'something_in_database' in your code
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

db=DATA_LISTE_IAGI()



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

    
    def loadFriendship_from_db(self,row)  : 
        self.establishFriendshipBetween(*row)
            
    def loadFriendships_from_db(self, db)  : 
        query = """
        select * from students_friendships 
        """
        rows=db.select_query(query) 
        for index,row in enumerate(rows) :
            if index%2!=0:
                self.loadFriendship_from_db(row)   
    
    def loadFriendship(self, friendships: list[list[float]]):
        for friendship in friendships :
            try :
                self.friendshipMatrix[friendship[0]-1][friendship[1]-1]=friendship[2] 
                self.friendshipMatrix[friendship[1]-1][friendship[0]-1]=friendship[2]
            except Exception as e :
                print(f"error establishing friendship : {e}")  
              
                
    def establishFriendshipBetween(self, user1Id: int, user2Id: int, coeff: float=.1 ):
        if user1Id <= self.num_students and user2Id <= self.num_students :
            self.friendshipMatrix[user1Id][user2Id]=coeff
            self.friendshipMatrix[user2Id][user1Id]=coeff 
        
            
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id][user2Id]
    



    def draw_social_graph(self,User : object)->object:  
        G = nx.Graph()
        G.add_nodes_from(User.Users[i].username for i in range(self.num_students)) # Add the nodes

        for student in range(self.num_students):
            for friend in range(student):
                if student != friend and self.friendshipMatrix[student][friend] != 0:
                    edge_weight = self.friendshipMatrix[student][friend]
                    G.add_weighted_edges_from([(User.Users[student].username, User.Users[friend].username, edge_weight)])
        return G 
    

    def draw_person_graph(self,User : object,user_id=None)->object:  
        G = nx.Graph()
        if user_id >self.num_students :
            print('student not enrolled in this class')
            return 
        G.add_node(User.Users[user_id-1].username)
        G.add_nodes_from(User.Users[i].username for i in range(self.num_students) if self.friendshipMatrix[user_id-1][i]!=0 and i!=user_id-1) # Add the nodes
        for friend in range(self.num_students):
                if user_id-1 != friend and self.friendshipMatrix[user_id-1 ][friend] != 0:
                    edge_weight = self.friendshipMatrix[user_id-1][friend]
                    G.add_weighted_edges_from([(User.Users[user_id-1].username, User.Users[friend].username, edge_weight)])
        return G   


    def show_customized_graphe(self,G:object) :
        edge_widths = {}

        # Iterate over edges and set width based on edge values
        for edge in G.edges(data=True):
            edge_data = edge[:-1] +tuple(edge[-1].items()) 
            edge_widths[edge_data] = edge[2].get('weight', 1.0) *CustomSettings.edge_weight_coif.value
        # Create a list of edge colors based on edge values
        edge_colors = [edge[2].get('color', 'black') for edge in G.edges(data=True)]
        pos = nx.spring_layout(G)  # You can choose other layout algorithms
        # Draw nodes
        nx.draw(
            G,
            pos,
            with_labels=CustomSettings.with_labels.value,
            node_size=CustomSettings.node_size.value,
            node_color=CustomSettings.node_color.value,
            font_color=CustomSettings.font_color.value,
            font_size=CustomSettings.font_size.value,  # Adjust the font size as needed
            font_family=CustomSettings.font_family.value,  # Choose the font family
            font_weight=CustomSettings.font_weight.value,  # Choose the font weight
            width=list(edge_widths.values()), #edges width
            edge_color=edge_colors # edges color
        )
        # Draw edges with weights
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)           
        # Display the graph
        plt.show()
    def save_png(self,filename) : #to save the  figure  (take the path as an argument)
        if not os.path.isfile(filename):
            plt.savefig(filename)
            print(f"Figure saved as {filename}")
        else:
            print(f"File '{filename}' already exists. Figure not saved to avoid overwriting.")


            
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
        plt.figure(figsize=(20,11))
        nx.draw(self.G, pos = pos, with_labels = True, node_color = colors, labels = labels, font_color = "black")

    def show(self):
        plt.show()

    def save(self, filename):
        plt.savefig(filename)
        
