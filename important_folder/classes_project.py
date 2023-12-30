import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
preferences = (('Sports', 1),
               ('Gaming', 2),
               ('Fitness', 3),
               ('Science_and_Education', 4),
               ('Music', 5),
               ('Lifestyle_and_travel', 6),
               ('Culinary_Arts', 7),
               ('Photography', 8),
               ('Parenting', 9),
               ('Fashion', 10),
               ('Other', 11))
list_IAGI=[ ('ismail   moufatih', 1),
            ('oussama  darrazi', 2),
            ('mohsine  mohsine', 3),
            ('yassin  ahmed', 4) ,
            ('ibrahim  goumrane', 5)]     
class Person:
    code_counter = 1  # Utilisation d'une variable de classe pour gérer le code de manière globale
    def __init__(self, nom, pref=None, amis=None, code=None ,black_list=[]):
        self.nom = nom
        self.code = Person.generate_code(code)
        self.pref = pref if pref is not None else []
        self.amis = amis if amis is not None else []
        self.black_list=black_list
        self.add_person_list()
    @classmethod
    def generate_code(cls, provided_code):
        if provided_code is not None:
            return provided_code
        else:
            generated_code = cls.code_counter
            cls.code_counter += 1
            return generated_code
    def add_person_list(self)  :
        list_IAGI.append((self.nom,self.code) if (self.nom,self.code) not in list_IAGI else None)      
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
    def get_friend(self,p1):
        return [list_IAGI[p1.code-1][i] for i in range(self.n) if self.matrice_amis[p1.code-1][i]!=0]        
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
def affichage_amis(p1,matrix,title):
    #ajout de titre
    plt.title(title)
    list_amis=np.array(matrix['mat_amis'][p1.code-1])
    
    G = nx.Graph()

    # Add edges from the adjacency matrix
    for j in range(len(list_amis)):
        if list_amis[j] != 0 and  p1.code-1 is not j:
            G.add_edge(list_IAGI[p1.code-1][0], list_IAGI[j][0], weight=list_amis[j])  # Use weights from the adjacency matrix

    # Visualize the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=7, font_color='black', font_weight='bold', edge_color='red', width=2.0, alpha=0.7)

    #visualize the edges values
    edgelabel=nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edgelabel)

    
    plt.show()    
    
def generate_deg_amis(matrice,code_src,code_inter,code_new) :
    return (matrice[code_src][code_inter]+matrice[code_inter][code_new])/2
def suggestin_friend_based_current_friend(p1,graphe):
    current_friend_list=[i for i in range(graphe.n) if graphe.get_matrix()['mat_amis'][p1.code-1][i]!=0 and i!= p1.code-1]
    for i in current_friend_list :
        current_friend_list_i=[j for j in range(graphe.n) if graphe.get_matrix()['mat_amis'][i][j]!=0 and i!=j]
        for j in current_friend_list_i :
            if j+1 not in p1.black_list and j not in current_friend_list and j+1!=p1.code:
                response=int(input(f'{list_IAGI[j][0]} this is a friend of {list_IAGI[i][0]} : do you want him to become your friend (1 or 0)'))
                if response==1 :
                    graphe.matrice_amis[p1.code-1][j]=generate_deg_amis(graphe.get_matrix()['mat_amis'],p1.code-1,i,j)
                    print(f'{list_IAGI[j+1][0]} ajouter a la liste des amis')                              
    title=f"Graph des nouveaux amis de {p1.nom}"                
    affichage_amis(p1,graphe.get_matrix(),title)      
  
    
# test data des personnes 
# deuxieme list correspond au activite et de degre de realisation de cette activites








    