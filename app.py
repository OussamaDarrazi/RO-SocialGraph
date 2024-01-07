#flask dependencies
from flask import Flask, redirect, render_template
#social media dependencies
from socialmedia import User as usr
from socialmedia.FriendSuggestionDelegate import FriendSuggestionDelegate
from socialmedia.SocialGraph import SocialGraph
from socialmedia.Interests import Interests
#defining users
usr.User(0,"Darrazi Oussama", {Interests.Music, Interests.Science_and_education, Interests.Culinary_arts})
usr.User(1,"Goumrane Ibrahim", {Interests.Gaming, Interests.Science_and_education, Interests.Science_and_education})
usr.User(2,"Moufatih Ismail", {Interests.Gaming, Interests.Music, Interests.Photography, Interests.Fitness, Interests.Science_and_education})
usr.User(3,"Miahi Othmane", {Interests.Lifestyle_and_travel})
usr.User(4,"Tahiri Meryem", {Interests.Culinary_arts})
usr.User(5,"Loro Triomphe", {Interests.Music})
usr.User(6,"Chaffaa Mohammed", {Interests.Parenting})
usr.User(7,"Dahouz Fatima", {Interests.Science_and_education})
graphe = SocialGraph(8)
#creation des amitiés
usr.User.Users[2].addFriend(usr.User.Users[4], graphe)
usr.User.Users[2].addFriend(usr.User.Users[1], graphe)
usr.User.Users[2].addFriend(usr.User.Users[5], graphe)
usr.User.Users[2].addFriend(usr.User.Users[7], graphe)

usr.User.Users[5].addFriend(usr.User.Users[3], graphe)
usr.User.Users[5].addFriend(usr.User.Users[6], graphe)

usr.User.Users[7].addFriend(usr.User.Users[3], graphe)
usr.User.Users[7].addFriend(usr.User.Users[6], graphe)
usr.User.Users[7].addFriend(usr.User.Users[5], graphe)

usr.User.Users[0].addFriend(usr.User.Users[5], graphe)
usr.User.Users[0].addFriend(usr.User.Users[3], graphe)
usr.User.Users[0].addFriend(usr.User.Users[1], graphe)

app = Flask(__name__)
uid=0
currentUser = usr.User.Users[uid]

@app.route("/")
def index():
    friends = currentUser.getFriends(graphe)
    suggestions = currentUser.suggestQueue.getSuggestionMemory()
    suggestion = suggestions[0][1] if len(suggestions) else None
    communFriends=[fr.username for fr in currentUser.getCommunFriends(suggestion, graphe)] if suggestion else None
    communInterests = [innt.name for innt  in currentUser.getCommunInterests(suggestion)] if suggestion else None
    graphe.render(usr.User.Users, uid)
    # graphe.show()
    graphe.save("./static/img/graphe.png")
    return render_template("index.html", currentUser = currentUser, friends=friends, suggestions=suggestions, suggestion = suggestion,communFriends=communFriends, communInterests=communInterests,graphe=graphe)

@app.route("/accept/<int:id>")
def accept(id):
    currentUser.addFriend(usr.User.Users[id], graphe)
    currentUser.suggestQueue.PopFriendSuggest()
    return redirect("/")

@app.route("/skip")
def skip():
    currentUser.suggestQueue.PopFriendSuggest()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)