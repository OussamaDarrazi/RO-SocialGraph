import heapq
from socialmedia.Interests import Interests
from socialmedia.SocialGraph import SocialGraph

class User:
    id_cnt=0
    Users = []
    def __init__(self, username: str, interests: list[Interests]) -> None:
        self.__suggestQueue = FriendSuggestionQueue()
        self.id = User.id_cnt
        User.id_cnt+=1
        self.username = username
        self.interests = interests
        User.Users.append(self)


    def addFriend(self, graph: SocialGraph):
        '''
        use establishFriendshipBetween from the graph to add friendship
        '''
        

    def getFriends(self, graph: SocialGraph) -> list:
        '''
        return list of of ids of friends
        '''
        

    def isFriendOf(self, user, graph: SocialGraph) -> bool:
        ...
        
    def getCommunInterests(self, user) -> list(Interests):

        ...

class FriendSuggestionQueue:
    def __init__(self) -> None:
        self.__suggestMemory = []

    def PushFriendSuggests(self, user: User, priority: float):
        '''
        implement a max heap/priority queue to push friends of friends into __suggestMemory
        '''

    def PopFriendSuggest(self) -> User:
        '''
        implement a max heap/priority queue to pop friends from friends into __suggestMemory
        '''

    def __len__(self):
        return len(self.__suggestMemory)
