import heapq
from socialmedia.Interests import Interests
from socialmedia.SocialGraph import SocialGraph

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


    def addFriend(self, friend,  graph: SocialGraph):
        coeff = .1 #TODO: calculating the friendship coefficient
        graph.establishFriendshipBetween(self.id, friend.id, coeff)

        #getting friends of friend to push them to suggestion memory
        friends_of_friend = friend.getFriends(graph)
        for frnd_of_frnd in friends_of_friend:
            priority_coeff = .1 #TODO: implement equation to calculate priority coefficient
            self.suggestQueue.PushFriendSuggests(frnd_of_frnd, priority_coeff)
        

    def getFriends(self) -> list:
        return [usr for usr in User.Users if self.isFriendOf(usr)]
            
        

    def isFriendOf(self, user, graph: SocialGraph) -> bool:
        return graph.getFriendshipCoeff(self.id, user.id)>0
    

    def getCommunInterests(self, user) -> set(Interests):
        return self.interests.intersection(user.interests)
        
#!!!!!!!!!!!!!!!important heapq is a min heap
class FriendSuggestionQueue:
    def __init__(self) -> None:
        self.__suggestMemory = []

    def PushFriendSuggests(self, user: User, priority: float):
        heapq.heappush(self.__suggestMemory, (1-priority, user))

    def PopFriendSuggest(self) -> User:
        return heapq.heappop(self.__suggestMemory)[1]

    def __len__(self):
        return len(self.__suggestMemory)
    
