from socialmedia import User as usr
from socialmedia.FriendSuggestionDelegate import FriendSuggestionDelegate
from socialmedia.SocialGraph import SocialGraph
from socialmedia.Interests import Interests
#defining users in 

user1 = usr.User("Oussama Darrazi", [Interests.Music, Interests.Science_and_education, Interests.Culinary_arts])
user2 = usr.User("Ibrahim Goumrane", [Interests.Gaming, Interests.Science_and_education])
user3 = usr.User("Ismail Moufatih", [Interests.Gaming, Interests.Music, Interests.Photography, Interests.Fitness])
user4 = usr.User("Name lastname1", [Interests.Lifestyle_and_travel])
user5 = usr.User("Name lastname2", [Interests.Culinary_arts])
user6 = usr.User("Name lastname3", [Interests.Music])
user7 = usr.User("Name lastname4", [Interests.Parenting])
user8 = usr.User("Name lastname5", [Interests.Other])




#testing userbase
for _ in usr.User.Users:
    print(_.username) 


#testing commun interests
user1.getCommunInterests(user2)
user4.getCommunInterests(user8)

#testing friendship functions


#TODO: add more tests





######################## MAIN APP #####################
#TODO: add main functionality