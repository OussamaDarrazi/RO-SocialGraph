#flask dependencies
from flask import Flask, redirect, render_template
#social media dependencies
from socialmedia import User as usr
from socialmedia.SocialGraph import SocialGraph
from socialmedia.Interests import Interests
#defining users

graphe = SocialGraph(15)
def friendships():
    """
    generer des utilisateurs, et des amities
    """
    import random
    usr.User(0,"Darrazi Oussama", {Interests.Music, Interests.Science_and_education, Interests.Culinary_arts})
    usr.User(1,"Goumrane Ibrahim", {Interests.Gaming, Interests.Science_and_education, Interests.Other})
    usr.User(2,"Moufatih Ismail", {Interests.Gaming, Interests.Music, Interests.Photography, Interests.Fitness, Interests.Science_and_education})
    usr.User(3,"Miahi Othmane", {Interests.Lifestyle_and_travel})
    usr.User(4,"Tahiri Meryem", {Interests.Culinary_arts})
    usr.User(5,"Loro Triomphe", {Interests.Music, Interests.Sports})
    usr.User(6,"Chaffaa Mohammed", {Interests.Lifestyle_and_travel, Interests.Gaming})
    usr.User(7,"Dahouz Fatima", {Interests.Science_and_education, Interests.Music, Interests.Parenting})
    usr.User(8, "Hajji Lamiaa", {Interests.Science_and_education, Interests.Fashion, Interests.Parenting})
    usr.User(9, "Mourad Taha", {Interests.Science_and_education, Interests.Other})
    usr.User(10, "Fikri Saad", {Interests.Culinary_arts, Interests.Fashion})
    usr.User(11, "Nadiri Nada", {Interests.Sports, Interests.Culinary_arts, Interests.Fitness})
    usr.User(12, "Chakir Achraf", {Interests.Music, Interests.Photography})
    usr.User(13, "Assiri Ikram", {Interests.Lifestyle_and_travel, Interests.Fashion, Interests.Music})
    usr.User(14, "Khaidar Ibrahim", {Interests.Gaming, Interests.Fashion, Interests.Music})
    #creation des amitiés
    print(len(usr.User.Users))
    for i in range(13, -1, -1):
        uid1 = i
        for j in range(random.randint(2, 5)): #creer entre 1 est 3 amis
            uid2=random.randint(i+1, 14)
            usr.User.Users[uid1].addFriend(usr.User.Users[uid2], graphe)


friendships()
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