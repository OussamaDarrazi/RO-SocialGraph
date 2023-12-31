import sys
from pathlib import Path

# Add the directory containing 'database' to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Now you can import from 'database'
from database.date_base_etudiant_iagi import DATA_LISTE_IAGI

# Use 'something_in_database' in your code
import networkx as nx
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
        else :
            print("{},{}student not enrolled in this class".format(user1Id,user2Id))    
        print("operation done .")
            
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id-1][user2Id-1]
     
      
        
        
liste_iagi=SocialGraph(62) 