import sys
from pathlib import Path

# Add the directory containing 'database' to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Now you can import from 'database'
from database.date_base_etudiant_iagi import DATA_LISTE_IAGI

# Use 'something_in_database' in your code
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import User as usr




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
    def draw_social_graph(self):
        G = nx.DiGraph()
        G.add_nodes_from(usr.User.Users[i].username for i in range(self.num_students)) # Add the nodes

        for student in range(self.num_students):
            for friend in range(student):
                if student != friend and self.friendshipMatrix[student][friend] != 0:
                    edge_weight = self.friendshipMatrix[student][friend]
                    G.add_weighted_edges_from([(usr.User.Users[student].username, usr.User.Users[friend].username, edge_weight)])

        pos = nx.spring_layout(G)  # You can choose other layout algorithms
        # Draw nodes
        nx.draw(G, pos, with_labels=True, node_size=400, node_color="green")

        # Draw edges with weights
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        # Display the graph
        plt.show()

            
      
        
        
liste_iagi=SocialGraph(8) 
liste_iagi.loadFriendships_from_db()
print(liste_iagi.friendshipMatrix)
liste_iagi.draw_social_graph()