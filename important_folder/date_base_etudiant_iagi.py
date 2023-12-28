import sqlite3 
import pandas as pd


liste_iagi_excel=pd.read_excel("liste_iagi_1.xlsx") #transform excel file into a pandas data frame
class data_listeIagi :
    def __init__(self):
        self.db=sqlite3.connect("IAGI_class.db")
        self.cursor=self.db.cursor()
        self.create_table()
    def create_table(self) :
        self.cursor.execute("""create table if not exists liste_IAGI(
                            code number,
                            nom string ,
                            pref string , 
                            amis string )""")
    def add_etudiant_db(self,dataframe) :# cette partie s'occupe de ajoute du code et du nom prenom de etudiant dans la db
         # Itérer sur les lignes du DataFrame et insérer dans la base de données
        for index, row in dataframe.iterrows():
            # Ajuster la requête d'insertion selon votre table
            insert_query = f'''
                INSERT INTO liste_IAGI (code,nom)
                VALUES (?,?)
            '''
            # Exécuter la requête d'insertion avec les valeurs de la ligne actuelle
            self.cursor.execute(insert_query,(index,' '.join(list(row))) )
        self.db.commit()  
    def update_data_student(self,
                            values={"code_value":None,
                                    "changed_value":None,
                                    "New_value":None}):#update en cas de modification
        self.cursor.execute("update liste_IAGI set (?)=(?) where code = (?) ",(values["changed_value"],
                                                                               values["New_value"],
                                                                               values["code_value"]))     
        self.db.commit()
    def select_query(self,query):
        selected_values=self.cursor.execute(query).fetchall()
        return selected_values       
    def close_db(self):
        self.cursor.close()
        self.db.close()
our_data_base=data_listeIagi()            #to create your actual data base
# our_data_base.add_etudiant_db(liste_iagi_excel)         #to add element to your data base    
        
        
        
        
             