from socialmedia import User as usr
from socialmedia.FriendSuggestionDelegate import FriendSuggestionDelegate
from socialmedia.SocialGraph import SocialGraph
from socialmedia.Interests import Interests
# from socialmedia.UserFactory import UserFactory
#defining users in 

usr.User(0,"Darrazi Oussama", {Interests.Music, Interests.Science_and_education, Interests.Culinary_arts})
usr.User(1,"Goumrane Ibrahim", {Interests.Gaming, Interests.Science_and_education})
usr.User(2,"Moufatih Ismail", {Interests.Gaming, Interests.Music, Interests.Photography, Interests.Fitness})
usr.User(3,"Miahi Othmane", {Interests.Lifestyle_and_travel})
usr.User(4,"Tahiri Meryem", {Interests.Culinary_arts})
usr.User(5,"Loro Triomphe", {Interests.Music})
usr.User(6,"Chaffaa Mohammed", {Interests.Parenting})
usr.User(7,"Dahouz Fatima", {Interests.Other})


graphe = SocialGraph(8)


#creation des amitiés

usr.User.Users[0].addFriend(usr.User.Users[3], graphe)
usr.User.Users[0].addFriend(usr.User.Users[5], graphe)
usr.User.Users[0].addFriend(usr.User.Users[1], graphe)

usr.User.Users[2].addFriend(usr.User.Users[4], graphe)
usr.User.Users[2].addFriend(usr.User.Users[1], graphe)
usr.User.Users[2].addFriend(usr.User.Users[5], graphe)
usr.User.Users[2].addFriend(usr.User.Users[7], graphe)

usr.User.Users[5].addFriend(usr.User.Users[3], graphe)
usr.User.Users[5].addFriend(usr.User.Users[6], graphe)

usr.User.Users[7].addFriend(usr.User.Users[3], graphe)
usr.User.Users[7].addFriend(usr.User.Users[6], graphe)
usr.User.Users[7].addFriend(usr.User.Users[5], graphe)

