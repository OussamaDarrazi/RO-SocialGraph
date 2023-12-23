from enum import Enum

class MediaType(Enum):
    Video = 0
    Image = 1
    Post = 3
#test

class Interets(Enum):
    Sports = "sports"
    Gaming = "gaming"
    Fitness = "fitness"
    Science_and_Education = "science and education"
    Music = "music"
    Lifestyle_and_travel = "lifestyle and travel"
    Culinary_Arts = "culinary arts"
    Photography = "photography"
    Parenting = "parenting"
    Fashion = "fashion"
    Other = "other"


class Content:
    last_id=0
    def __init__(self, type=MediaType.Post, interet=Interets.Other):
        self.id = Content.last_id
        Content.last_id+=1
        self.type = type
        self.interet = interet
        self.vues=0
        self.vu_par = [] #list d'utilisateur qui ont consulté cette piece de contenu

class ContentDelegate:
    #class singleton parcequ'on peut avoir un seul delegue de contenu
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContentDelegate, cls).__new__(cls)
            # Init ici
        return cls._instance
    def add_content_to_content_base(self, content: Content):
        #TODO: ajouter la piece de contenu dans la base
        pass

    def suggest_content(self, user_id):
        #TODO:
        # Consulter la list des pieces de contenu
        # Trouver les mieux convenable a suggerer
        # suggerer les pieces dont le user n'a pas encore consulté
        pass


class User:
    last_id=0
    def __init__(self, name: str, age: int, location ,interets: dict = None):
        self.id = User.last_id
        User.last_id+=1 #pour changer l'id pour le prochain utilisateur
        self.loc = location
        self.name = name
        self.age = age
    def add_friend(self, friend_id: int):
        #TODO: modifier le graphe d'amitié graphe[self.id][friend_id]
        pass

    def like_content(self, content_id: int):
        #TODO: implementer mechanisme de like est increment l(es) interest(s) en question
        pass



############################################
#TEST et exemple

user1 = User("test test", 20, "Sidi othman", {Interets.Gaming: 4, Interets.Music: 2, Interets.Science_and_Education:1, Interets.Sports: 1})

cnt1 = Content(MediaType.Video, Interets.Music)
cnt2 = Content(MediaType.Video, Interets.Fashion)
cnt3 = Content(MediaType.Video, Interets.Gaming)
cnt4 = Content(MediaType.Video, Interets.Sports)

cnt_dlg = ContentDelegate()


#ajouter les pieces de contenu a la base
cnt_dlg.add_content_to_content_base(cnt1)
cnt_dlg.add_content_to_content_base(cnt2)
cnt_dlg.add_content_to_content_base(cnt3)
cnt_dlg.add_content_to_content_base(cnt4)

#suggerer les pieces de contenus
cnt_dlg.suggest_content(user1.id)
# output:   cnt3 (puisque user1 a 4 score gaming)

cnt_dlg.suggest_content(user1.id)
# output:   cnt1 (gaming est deja suggerer, alors suggerer music)

user1.like_content(cnt2.id)

cnt_dlg.suggest_content(user1.id)
#output: cnt2 ou cnt4 (puisque l'utilisateur a aimé une piece de contenu fashion)

b1=ContentDelegate()
b2=ContentDelegate()
print(b1 is b2)