import heapq
from socialmedia.Interests import Interests
from socialmedia.SocialGraph import SocialGraph
import random

class User:
    id_cnt=0
    Users = []
    def __init__(self, id=None, username: str="", interests: set[Interests]=set()) -> None:
        self.suggestQueue = FriendSuggestionQueue()
        self.id = id
        # self.id = User.id_cnt
        # User.id_cnt+=1
        self.username = username
        self.interests = interests
        User.Users.append(self)

    def __lt__(self, other):
        """
        pour comparer les utilisateurs a la base de leurs id (utilisé par la file)
        """
        return self.id < other.id

    def addFriend(self, friend,  graph: SocialGraph):
        coeff = round(random.random(), ndigits=2) #TODO: calculating the friendship coefficient
        graph.establishFriendshipBetween(self.id, friend.id, coeff)
        #removing from queue if it's there
        if friend in self.suggestQueue:
            self.suggestQueue.removeUser(friend)
        #getting friends of friend to push them to suggestion memory
        friends_of_friend = friend.getFriends(graph)
        for frnd_of_frnd in friends_of_friend:
            if frnd_of_frnd.id != self.id and not self.isFriendOf(frnd_of_frnd, graph) and frnd_of_frnd not in self.suggestQueue:
                priority_coeff = random.random() #TODO: implement equation to calculate priority coefficient
                self.suggestQueue.PushFriendSuggests(frnd_of_frnd, priority_coeff)
        

    def getFriends(self, graph) -> list:
        return {usr for usr in User.Users if self.isFriendOf(usr, graph)}
            

    def isFriendOf(self, user, graph: SocialGraph) -> bool:
        if self is user:
            return False
        return graph.getFriendshipCoeff(self.id, user.id)>0
    
    def getCommunFriends(self, user, graph) -> set:
        return self.getFriends(graph).intersection(user.getFriends(graph))


    def getCommunInterests(self, user) -> set(Interests):
        return self.interests.intersection(user.interests)
        
#!!!!!!!!!!!!!!!important heapq is a min heap
class FriendSuggestionQueue:
    def __init__(self) -> None:
        self.__suggestMemory = []

    def __contains__(self, item):
        """
        pour verifier si la file contient un element en utilisant l'operateur 'in'
        """
        return any(item in _ for _ in self.__suggestMemory)
    
    def getSuggestionMemory(self):
        return self.__suggestMemory
    
    def removeUser(self, user):
        """
        pour eliminer des utilisateurs qe la file a volonté
        """
        self.__suggestMemory = [(_, usr) for _, usr in self.__suggestMemory if usr != user]

    def PushFriendSuggests(self, user: User, priority: float):
        heapq.heappush(self.__suggestMemory, (round(1-priority, ndigits=2), user))

    def PopFriendSuggest(self) -> User:
        return heapq.heappop(self.__suggestMemory)[1]

    def __len__(self):
        return len(self.__suggestMemory)
    


