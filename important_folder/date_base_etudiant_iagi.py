import sqlite3 
import pandas as pd
import json


liste_iagi_excel=pd.read_excel("liste_iagi_1.xlsx") #transform excel file into a pandas data frame




class DATA_LISTE_IAGI :
    def __init__(self):
        self.db=sqlite3.connect("IAGI_class.db")
        self.cursor=self.db.cursor()
        self.create_table()
        
        
        
    def close_connection(self):
        #close the data base connection
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()  
    def create_table(self) :
        self.cursor.execute("""create table if not exists liste_IAGI(
                            id string primary key ,
                            name string ,
                            pref string , 
                            amis string )""")
    def add_student(self, name=None, id=None, pref=None, amis=None):
        """ 
        Add one student.
        The use of %s is for handling non-entered values, setting them to NULL in the table.
        """
        try:
            # Serialize the list of friends to a JSON string
            amis_json = json.dumps(amis)
            self.cursor.execute("INSERT INTO liste_IAGI (id, name, pref, amis) VALUES (?, ?, ?, ?)", (id, name, pref, amis_json))
            self.db.commit()
        except Exception as e:
            # Handle the exception
            print(f"Error adding student: {e}")
            self.db.rollback()  # Rollback the transaction to maintain data consistency
        """
        to retreive the string in form of a list
        amis_json_from_db = liste_iagi['amis']
        amis_list = json.loads(amis_json_from_db)
        """
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
            self.cursor.execute(insert_query,(str(index),' '.join(list(row))) )
        self.db.commit()  
        
        
        
    def update_data_student(self,id_value=None,changed_value=None,New_value=None) :
        #update en cas de modification
        self.cursor.execute("UPDATE liste_IAGI SET {} = ? WHERE id = ?".format(changed_value),
                        (New_value, str(id_value)))
        self.db.commit()
        
        
    def select_query(self,query):
        selected_values=self.cursor.execute(query).fetchall()
        return selected_values      




our_data_base=DATA_LISTE_IAGI()            #to create your actual data base
our_data_base.add_student_df(liste_iagi_excel)         #to add element to your data base    


"""
        # Assuming you have a list of students, where each student is represented as a tuple
students_to_add = [
    ('John Doe', 62, 'Science', ['50', '30']),
    ('Jane Smith', 63, 'Art', ['40', '20']),
    ('Alex Johnson', 64, 'Math', ['2', '1']),
    # ... add more students as needed
]

# Now, you can use the add_students method
our_data_base.add_students(students_to_add)
our_data_base.update_data_student(1,"name","yassin ahmed")   #the modification test          
""" 
  