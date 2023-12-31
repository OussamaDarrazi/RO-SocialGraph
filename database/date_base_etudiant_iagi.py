import sqlite3 
import random




class DATA_LISTE_IAGI :
    _instance=None # in order to know if an object has already been initialize
    def __new__(cls) -> None:
        if cls._instance is None :
            DATA_LISTE_IAGI._instance=super(DATA_LISTE_IAGI,cls).__new__(cls)
        return DATA_LISTE_IAGI._instance 
    
    def __init__(self):
        self.db=sqlite3.connect("database/IAGI_class.db")
        self.cursor=self.db.cursor()
        self.create_table()
        
    def __del__(self):
        #close the data base connection
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close() 
            
            
            
    #creation des table de la  data base         
    def create_table(self) :
        self.cursor.execute("""create table if not exists liste_IAGI(
                            id int primary key ,
                            name string ,
                            CONSTRAINT liste_amis_fk foreign key(id) references students_friendships(id_person),
                            CONSTRAINT liste_amis_fk foreign key(id) references preferences(id_person))
                            """)
        self.cursor.execute("""
                            create table if not exists students_friendships(
                            id_person int not null,
                            id_friend int not null,
                            friendship_deg int not null,
                            CONSTRAINT students_friendships_amis_fk foreign key(id_friend)  references liste_IAGI (id) )
                            """)
        self.cursor.execute("""
                            create table if not exists preferences(
                            id_person int primary key, 
                            Sports int not null,
                            Gaming int not null,
                            Fitness int not null,
                            Science_and_education int not null,
                            Music int not null,
                            Lifestyle_and_travel int not null,
                            Culinary_arts int not null,
                            Photography int not null,
                            Parenting int not null,
                            Fashion int not null,
                            Other int not null
                            )
                             """)
    
    
    
    #initialiser la table liste_IAGI       
    def add_student(self, name=None, id=None, pref=None, amis=None):
        """ 
        Add one student.
        The use of %s is for handling non-entered values, setting them to NULL in the table.
        """
        try:
            # Serialize the list of friends to a JSON string
            self.cursor.execute("INSERT INTO liste_IAGI (id, name, pref, amis) VALUES (?, ?)", (id, name))
            self.db.commit()
        except Exception as e:
            # Handle the exception
            print(f"Error adding student: {e}")
            self.db.rollback()  # Rollback the transaction to maintain data consistency
            
              
    def add_students(self, list_of_students):
        for student_info in list_of_students:
            self.add_student(*student_info)
        
        

    def add_student_df(self,dataframe) : 
        """
         cette partie s'occupe de ajoute du id et du name prename de etudiant dans la db
         Itérer sur les lignes du DataFrame et insérer dans la base de données
         """
        for index, row in dataframe.iterrows():
            # Ajuster la requête d'insertion selon votre table
            insert_query = f'''
                INSERT INTO liste_IAGI (id,name)
                VALUES (?,?)
            '''
            # Exécuter la requête d'insertion avec les valeurs de la ligne actuelle
            self.cursor.execute(insert_query,(index+1,' '.join(list(row))) )
        self.db.commit()  
        
        
        
    def update_data_student(self,id_value=None,changed_value=None,New_value=None) :
        #update en cas de modification
        self.cursor.execute("UPDATE liste_IAGI SET {} = ? WHERE id = ?".format(changed_value),
                        (New_value, id_value))
        self.db.commit()
        
        
    def select_query(self,query):
        selected_values=self.cursor.execute(query).fetchall()
        return selected_values   
    
    
    
    # initialistion de table preference 
    def initialiser_preference(self, id=None):
        # Générer une liste de 11 valeurs aléatoires (0 ou 1)
        liste = [random.randint(0, 1) for _ in range(11)]
        try :
            # Utiliser une requête SQL paramétrée pour insérer les valeurs dans la base de données
            self.cursor.execute("""
                INSERT INTO preferences 
                (id_person, Sports, Gaming, Fitness, Science_and_education, Music, Lifestyle_and_travel, Culinary_arts, Photography, Parenting, Fashion, Other)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (id, *liste))
        except Exception as e :
            print(f"error adding preference :{e}")  
            self.db.rollback()
            return       
        self.db.commit()   
    def initialiser_preferences(self,number_of_students) :
         for i in range(1,number_of_students+1):
             self.initialiser_preference(i)    
           
           
             
    #initialiser la table friendship  
    def generation_aleatoire_amis(self, id):
        class FRIEND:
            def __init__(self, id_friend, friendship_deg):
                self.id_friend = id_friend
                self.friendship_deg = friendship_deg

        # Obtenir la liste des amis actuels de la personne
        current_friends = set()
        self.cursor.execute("""
            SELECT id_friend FROM students_friendships WHERE id_person = ?
        """, (id,))
        
        for row in self.cursor.fetchall():
            current_friends.add(row[0])

        # Générer une nouvelle liste d'amis excluant ceux qui sont déjà des amis
        new_friends = []
        num_friends = random.randrange(1, 5, 1)

        while len(new_friends) < num_friends:
            id_friend = random.randrange(1, 62, 1)
            generated_friends=set()
            friendship_deg=round(random.random(),2)
            # S'assurer que l'ami n'est pas déjà un ami et n'est pas la personne elle-même
            if id_friend != id and id_friend not in current_friends and id_friend not in generated_friends:
                friendship_deg = round(random.random(), 2)
                new_friends.append(FRIEND(id_friend, friendship_deg))
            generated_friends.add(id_friend)
        return [id, new_friends]
    def initialiser_friendship(self, id):
        # Génération des amis de la personne qui possède l'id
        friendship = self.generation_aleatoire_amis(id)
        try:
            # Utiliser une requête SQL paramétrée pour insérer les valeurs dans la base de données
            for friend in friendship[1]:
                self.cursor.execute("""
                    INSERT INTO students_friendships 
                    (id_person, id_friend, friendship_deg)
                    VALUES (?, ?, ?)
                """, (friendship[0], friend.id_friend, friend.friendship_deg))
                
                # Ajouter également l'amitié dans l'autre sens
                self.cursor.execute("""
                    INSERT INTO students_friendships 
                    (id_person, id_friend, friendship_deg)
                    VALUES (?, ?, ?)
                """, (friend.id_friend, friendship[0], friend.friendship_deg))
                
            self.db.commit()
        except Exception as e:
            print(f"Error adding friend: {e}")
            self.db.rollback()
    def initialiser_friendships(self,number_of_students)    :
        for id in range(number_of_students) :
            self.initialiser_friendship(id+1)
        self.cursor.execute("select * from students_friendships ORDER BY id_person asc")    


""" 
our_data_base.add_student_df(liste_iagi_excel)         #to add element to your data base    
our_data_base.initialiser_preferences(62)
our_data_base.initialiser_friendships(62)      
"""