preferences = {
    'Sports': 1, # chaque numero correspond a l'indice de chaque activites
    'Gaming': 2,
    'Fitness': 3,
    'Science_and_Education': 4,
    'Music': 5,
    'Lifestyle_and_travel': 6,
    'Culinary_Arts': 7,
    'Photography': 8,
    'Parenting': 9,
    'Fashion': 10,
    'Other': 11  # I added 'Other' with a value of 11, assuming it's the last option
}     
class Person:
    code_counter = 1  # Utilisation d'une variable de classe pour gérer le code de manière globale

    def __init__(self, nom, pref=None, amis=None, code=None):
        self.nom = nom
        self.code = Person.generate_code(code)
        self.pref = pref if pref is not None else []
        self.amis = amis if amis is not None else []

    @classmethod
    def generate_code(cls, provided_code):
        if provided_code is not None:
            return provided_code
        else:
            generated_code = cls.code_counter
            cls.code_counter += 1
            return generated_code

    def get_code(self):
        return self.code 
    
    
      
class graphe :
    n=0
    def __init__(self,taille):
        graphe.n=taille
        self.matrice_amis=[[0]*graphe.n for i in range(graphe.n)] # matrice representant les amis
        self.rel_person_preference=[[0]*len(preferences) for i in range(graphe.n)] # relation person preference
    def increment_num_matrice(self,p1) :# incrementer la taille de la matrice par 1 en cas d'ajout d'un element
        for i in self.matrice_amis :
            i.append(0)
        graphe.n+=1
        self.matrice_amis.append([0]*graphe.n)
        self.rel_person_preference.append([0]*len(preferences))         
    def get_relation(self,p1,p2):
        return self.matrice_amis[p1.code][p2.code]
    def set_amis(self,p1,exsists=True) : 
        n=p1.code if exsists else graphe.n
        for i in p1.amis :
            self.matrice_amis[n-1][i-1]= 1 # 1 c'est a dire amis 0 c'est a dire il ne sont pas amis
            self.matrice_amis[i-1][n-1]= 1  
    def set_person_preference(self,p1,exsists=True): 
        n=p1.code if exsists else graphe.n
        for i in p1.pref:
            self.rel_person_preference[n-1][i[0]]=i[1]                       
    def add_ele(self,p1,exsist=True): 
        self.increment_num_matrice(p1) if not exsist else None
        self.set_amis(p1,exsist) 
        self.set_person_preference(p1,exsist)     
    def get_mean(self) :
        mean=0
        for i in self.rel_person_preference :
            for j in i :
                mean+=j
        return mean/self.n**2 
    def get_matrix(self):# pour faire affichage des matrice
        return  {
            'mat_amis':self.matrice_amis,
            'mat_pref':self.rel_person_preference,
        }
    
# test data des personnes 

# deuxieme list correspond au activite et de degre de realisation de cette activites





    