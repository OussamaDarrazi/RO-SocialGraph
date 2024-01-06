import heapq
from Interests import Interests
from SocialGraph import SocialGraph

from database.date_base_etudiant_iagi import DATA_LISTE_IAGI

db=DATA_LISTE_IAGI()
class User:
    id_cnt=0
    Users = []
    class_student=SocialGraph()

    @classmethod
    def loadFriendship_from_db(cls,friends)  : 
        for friend in friends :
            User.class_student.establishFriendshipBetween(*friend)
            
    def loadFriendships_from_db()  : 
        for id_person in range(1,User.class_student.num_students+1)  :
            query_friends="""
                select * from students_friendships 
                where id_person={}
                """.format(id_person)
            friends=db.select_query(query_friends) 
            User.loadFriendship_from_db(friends)
            User.Users[id_person-1].addFriend(friends)



    def __init__(self, id=None, username: str="", interests: set[Interests]=set()) -> None:
        self.suggestQueue = FriendSuggestionQueue()
        self.id = id
        # self.id = User.id_cnt
        # User.id_cnt+=1
        self.username = username
        self.interests = interests
        User.Users.append(self)
        


    def addFriend(self, friends):
        coeff = .1 #TODO: calculating the friendship coefficient
        for id,friend,coif_friendship in friends :
            #getting friends of friend to push them to suggestion memory
            friends_of_friend =  User.Users[friend-1].getFriends()
            for frnd_of_frnd in friends_of_friend:
                priority_coeff = .1 #TODO: implement equation to calculate priority coefficient
                self.suggestQueue.PushFriendSuggests(frnd_of_frnd, priority_coeff)
            


    def getFriends(self) -> list:
        return [usr for usr in User.Users if self.isFriendOf(usr)]
            
        


    def isFriendOf(self, user) -> bool:
        return User.class_student.getFriendshipCoeff(self.id, user.id)>0
    


    def getCommunInterests(self, user) -> set(Interests):
        return self.interests.intersection(user.interests)
 




#!!!!!!!!!!!!!!!important heapq is a min heap
class FriendSuggestionQueue:
    def __init__(self) -> None:
        self.__suggestMemory = []

    def get_suggestMemory(self):
        return self.__suggestMemory
    def PushFriendSuggests(self, user: User, priority: float):
        heapq.heappush(self.__suggestMemory, (-priority, user.id))

    def PopFriendSuggest(self) -> User:
        return heapq.heappop(self.__suggestMemory)[1]

    def __len__(self):
        return len(self.__suggestMemory)
    



