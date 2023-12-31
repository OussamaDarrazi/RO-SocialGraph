from socialmedia import User as usr
from socialmedia.FriendSuggestionDelegate import FriendSuggestionDelegate
from socialmedia.SocialGraph import SocialGraph
from socialmedia.Interests import Interests
from UserFactory import UserFactory
#defining users in 

# usr.User(1,"Darrazi Oussama", {Interests.Music, Interests.Science_and_education, Interests.Culinary_arts})
# usr.User(2,"Goumrane Ibrahim", {Interests.Gaming, Interests.Science_and_education})
# usr.User(3,"Moufatih Ismail", {Interests.Gaming, Interests.Music, Interests.Photography, Interests.Fitness})
# usr.User(4,"Name lastname1", {Interests.Lifestyle_and_travel})
# usr.User(5,"Name lastname2", {Interests.Culinary_arts})
# usr.User(6,"Name lastname3", {Interests.Music})
# usr.User(7,"Name lastname4", {Interests.Parenting})
# usr.User(8,"Name lastname5", {Interests.Other})

UserFactory.usersFromDB()

#testing userbase
for _ in usr.User.Users:
    print(_.id, _.username) 



#testing commun interests

#testing friendship functions


#TODO: add more tests





######################## MAIN APP #####################
#TODO: add main functionality