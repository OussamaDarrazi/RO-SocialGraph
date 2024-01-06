import User as usr
import database.date_base_etudiant_iagi as db
from SocialGraph import SocialGraph
from Interests import Interests


class UserFactory:
    @staticmethod
    def userFromRow(row):
        interest_set = set([Interests(index+1) for index, val in enumerate(row[2:]) if val == 1])
        return usr.User(row[0], row[1], interest_set)
        
    @staticmethod
    def usersFromDB(db, graph):
        qr = """
        select e.id, e.name, i.Sports, i.Gaming, i.Fitness, i.Science_and_education, i.Music, i.Lifestyle_and_travel, i.Culinary_arts, i.Photography, i.Parenting, i.Fashion, i.Other
        from liste_IAGI as e 
        INNER JOIN preferences as i on e.id = i.id_person
        order by e.id
        """
        rows = db.select_query(qr)
        #creating the users
        for row in rows:
            """ the users are in the static attribute of User and can be called by index"""
            UserFactory.userFromRow(row)

        #sorting friendships
        qr = """
            select * from students_friendships
            """
        rows = db.select_query(qr)
        #initializing the graph
        graph.loadFriendships_from_db(db)
        #main purpose is to fill the queues for each user
        for row in rows:
            usr.User.Users[row[0]-1].addFriend(usr.User.Users[row[1]-1], graph)
        
    
# UserFactory.usersFromDB()    
# liste_iagi=SocialGraph(62) 
# liste_iagi.loadFriendships_from_db()
# G=liste_iagi.draw_person_graph(usr.User,14)
# liste_iagi.show_customized_graphe(G)



    
