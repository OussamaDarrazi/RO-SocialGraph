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





db=DATA_LISTE_IAGI()

class SocialGraph:
    def __init__(self,num_students) -> None:
        self.num_students=num_students
        self.friendshipMatrix =self.matrice_initialisation()  # creation of the friendship matrix initialised by 0
        
    def matrice_initialisation(self)  :
        matrix=[[0]*self.num_students for _ in range(self.num_students)]
        for i in range(self.num_students):
           matrix[i][i] = 1
        return   matrix

    
    def loadFriendship_from_db(self,row)  : 
        self.establishFriendshipBetween(*row)
            
    def loadFriendships_from_db(self)  : 
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
            self.friendshipMatrix[user1Id-1][user2Id-1]=coeff
            self.friendshipMatrix[user2Id-1][user1Id-1]=coeff 
        print("operation done .")
            
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id-1][user2Id-1]
    def draw_social_graph(self,User : object):
        
        G = nx.Graph()
        G.add_nodes_from(User.Users[i].username for i in range(self.num_students)) # Add the nodes

        for student in range(self.num_students):
            for friend in range(student):
                if student != friend and self.friendshipMatrix[student][friend] != 0:
                    edge_weight = self.friendshipMatrix[student][friend]
                    G.add_weighted_edges_from([(User.Users[student].username, User.Users[friend].username, edge_weight)])

        pos = nx.spring_layout(G)  # You can choose other layout algorithms
        # Draw nodes
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=600,
            node_color="green",
            font_color="black",
            font_size=5,  # Adjust the font size as needed
            font_family='sans-serif',  # Choose the font family
            font_weight='bold',  # Choose the font weight
        )

        # Draw edges with weights
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        choice =int(input("save the graphe type not 0")) 
        if choice :
            self.save_png("./socialmedia/photo.png")            
        # Display the graph
        plt.show()
    def save_png(self,filename) : #to save the  figure  (take the path as an argument)
        if not os.path.isfile(filename):
            plt.savefig(filename)
            print(f"Figure saved as {filename}")
        else:
            print(f"File '{filename}' already exists. Figure not saved to avoid overwriting.")


            
      
        
