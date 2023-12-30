from socialmedia.User import User


class FriendSuggestionDelegate:
    #pas de besoin d'instance
    @staticmethod
    def suggestFriend(user: User):
        '''
        use the friend suggestion queue to pop friend suggestion
        '''
        return user.suggestQueue.PopFriendSuggest()
