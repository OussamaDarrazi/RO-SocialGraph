import networkx as nx
import matplotlib.pyplot as plt
class SocialGraph:
    
    _instance=None # in order to know if an object has already been initialize
    def __new__(cls) -> None:
        if cls._instance is None :
            SocialGraph._instance=super(SocialGraph,cls).__new__(cls)
        return SocialGraph._instance    
    
    def __init__(self,num_students) -> None:
        self.num_student=num_students
        self.friendshipMatrix =self.matrice_0_initialisation()  # creation of the friendship matrix initialised by 0
        self.diagonal_1_initialisation()
        
    def matrice_0_initialisation(self)  :
        return  [[0]*self.num_students for _ in range(self.num_students)] 
    
    
    def diagonal_1_initialisation(self) :
        for i in range(self.num_student):
            self.friendshipMatrix[i][i] = 1
            
            
    def loadFriendship_from_db(self,db_object)  : 
        pass      
    
    def loadFriendship(self, friendships: list[list[float]]):
        for friendship in friendships :
            try :
                self.friendshipMatrix[friendship[0]][friendship[1]]=friendship[2] 
                self.friendshipMatrix[friendship[1]][friendship[0]]=friendship[2]
            except Exception as e :
                print(f"error establishing friendship : {e}")  
              
                
    def establishFriendshipBetween(self, user1Id: int, user2Id: int, coeff: float=.1):
        if user1Id <self.num_student and user2Id < self.num_student :
            self.friendshipMatrix[user1Id][user2Id]=coeff
            self.friendshipMatrix[user2Id][user1Id]=coeff
        else :
            print("student not enrolled in this class")    
        print("operation done .")
            
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        return self.friendshipMatrix[user1Id][user2Id]
     
      
        
        
liste_iagi=SocialGraph(62)    
liste_iagi.loadFriendship([[1,2,0.9]
                                    ,[2,3,0.5]])   