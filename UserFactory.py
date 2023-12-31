from socialmedia import User as usr
import important_folder.date_base_etudiant_iagi as db
from socialmedia.Interests import Interests

db = db.DATA_LISTE_IAGI()

class UserFactory:
    @staticmethod
    def userFromRow(row):
        interest_set = set([Interests(index+1) for index, val in enumerate(row[2:]) if val == 1])
        return usr.User(row[0], row[1], interest_set)
        
    
    def usersFromDB():
        qr = """
        select e.id, e.name, i.Sports, i.Gaming, i.Fitness, i.Science_and_education, i.Music, i.Lifestyle_and_travel, i.Culinary_arts, i.Photography, i.Parenting, i.Fashion, i.Other
        from liste_IAGI as e 
        INNER JOIN preferences as i on e.id = i.id_person
        order by e.id
        """
        rows = db.select_query(qr)
        for row in rows:
            """ the users are in the static attribute of User and can be called by index"""
            UserFactory.userFromRow(row)
        
    




    