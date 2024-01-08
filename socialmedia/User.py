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
    
    def calculateFriendshipCoefficient(self, friend, graph):
        """
        Calculate friendship coefficient based on shared interests and common friends.
        Adjust the weights based on the importance of each factor.
        """
        shared_interests_weight = 0.6
        common_friends_weight = 0.4
    
        shared_interests = len(self.getCommunInterests(friend))
        common_friends = len(self.getCommunFriends(friend, graph))

        # Normalize values between 0 and 1
        shared_interests_normalized = shared_interests / len(self.interests)
        common_friends_normalized = common_friends / len(User.Users)

        # Calculate friendship coefficient
        friendship_coefficient = (
            shared_interests_weight * shared_interests_normalized +
            common_friends_weight * common_friends_normalized
        )

        return friendship_coefficient
    
    def addFriend(self, friend,  graph: SocialGraph):
        coeff = self.calculateFriendshipCoefficient(friend, graph)
        graph.establishFriendshipBetween(self.id, friend.id, coeff)
        #removing from queue if it's there
        if friend in self.suggestQueue:
            self.suggestQueue.removeUser(friend)
        #getting friends of friend to push them to suggestion memory
        friends_of_friend = friend.getFriends(graph)
        for frnd_of_frnd in friends_of_friend:
            if frnd_of_frnd.id != self.id and not self.isFriendOf(frnd_of_frnd, graph) and frnd_of_frnd not in self.suggestQueue:
                priority_coeff = random.random()
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
        self.__suggestMemory = [(_, usr) for (_, usr) in self.__suggestMemory if usr != user]

    def PushFriendSuggests(self, user: User, priority: float):
        heapq.heappush(self.__suggestMemory, (round(1-priority, ndigits=2), user))

    def PopFriendSuggest(self) -> User:
        return heapq.heappop(self.__suggestMemory)[1]

    def __len__(self):
        return len(self.__suggestMemory)
    


