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
class person() :
    code=1
    def __init__(self,nom,pref :list,amis):
        self.non=nom
        self.code=person.code#code de correspondance dans la matrice
        person.code+=1
        self.pref=pref  #preference
        self.amis=amis#amis sous forme dun vecteur ligne
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
        n=p1.code if exsists else graphe.n-1
        for i in p1.amis :
            self.matrice_amis[n][i]= 1 # 1 c'est a dire amis 0 c'est a dire il ne sont pas amis  
    def set_person_preference(self,p1,exsists=True): 
        n=p1.code if exsists else graphe.n-1
        for i in p1.pref:
            self.rel_person_preference[n][i[0]]=i[1]                       
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
    def get_matrix(self):
        return  {
            'mat_amis':self.matrice_amis,
            'mat_pref':self.rel_person_preference,
        }
    
# test data des personnes 

# deuxieme list correspond au activite et de degre de realisation de cette activites



p1=person('ahmed',[[1,2],[3,5],[7,8],[5,2]],[4,8])
p2=person('ahmed',[[5,7],[2,4],[1,8]],[8])
p3=person('ahmed',[[8,5]],[2])
    
taille_IAGI=10
relation_p_class=graphe(taille_IAGI)


relation_p_class.add_ele(p1,False)    
relation_p_class.add_ele(p2,True)
relation_p_class.add_ele(p3,True) 
matrix=relation_p_class.get_matrix()
            

    