import sys
from pathlib import Path
import os
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
    num_students=None
    #we need only one instance of the socialgraphe class cause there is only one graphe
    _instance=None
    @classmethod
    # def __new__(cls, *args, **kwargs) -> object:
    #     if cls._instance is None :
    #         cls._instance=super(SocialGraph,cls).__new__(cls)
    #     return cls._instance    
    def __init__(self,num_students) -> None:
#      if not hasattr(self, 'initialized'):
            self.num_students=num_students
            SocialGraph.num_students=num_students
            self.friendshipMatrix =self.matrice_initialisation()  # creation of the friendship matrix initialised by 0
        
    def matrice_initialisation(self)  :
        matrix=[[0]*self.num_students for _ in range(self.num_students)]
        for i in range(self.num_students):
           matrix[i][i] = 1
        return   matrix
    def add_student_matrix(self): #to add more student dynamically to the matrix
        # Add a new row for the new student
        new_row = [0] * (SocialGraph.num_students + 1)
        self.friendshipMatrix.append(new_row)

        # Add a new column for the new student in existing rows
        for row in self.friendshipMatrix:
            row.append(0)

        # Update the number of students in the graph
        SocialGraph.num_students += 1
    def loadFriendship_from_db(self,friends)  : 
        for friend in friends :
            self.establishFriendshipBetween(*friend)
            
    def loadFriendships_from_db(self)  : 
        for id_person in range(1,self.num_students+1)  :
            query_friends="""
                select * from students_friendships 
                where id_person={}
                """.format(id_person)
            friends=db.select_query(query_friends) 
            self.loadFriendship_from_db(friends)      

    def loadFriendship(self, friendships: list[list[float]]):
        for friendship in friendships :
            try :
                self.friendshipMatrix[friendship[0]-1][friendship[1]-1]=friendship[2] 
                self.friendshipMatrix[friendship[1]-1][friendship[0]-1]=friendship[2]
            except Exception as e :
                print(f"error establishing friendship : {e}")  
              


    def establishFriendshipBetween(self, user1Id: int, user2Id: int, coeff: float=.1 ):
        if user1Id <= self.num_students and user2Id <= self.num_students :
            self.friendshipMatrix[user1Id-1][user2Id-1]=coeff
            self.friendshipMatrix[user2Id-1][user1Id-1]=coeff 
        print("operation done .")


    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id-1][user2Id-1]
    

                                    #drawing methods 
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





                        #test data
query='''
    select max(id) from liste_IAGI
'''
class_size=int((db.select_query(query))[0][0]) # to select the actual length of your class
liste_iagi=SocialGraph(class_size) 
liste_iagi.loadFriendships_from_db()            