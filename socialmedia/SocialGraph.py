class SocialGraph:
    def __init__(self) -> None:
        self.friendshipMatrix = []

    def loadFriendshipFromMatrix(self, mat: list[list[float]]):
        self.friendshipMatrix = mat
    
    def establishFriendshipBetween(self, user1Id: int, user2Id: int, coeff: float=.1):
        ...
    
    def getFriendshipCoeff(self, user1Id: int, user2Id: int) -> float:
        ...