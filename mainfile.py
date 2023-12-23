from classes_project import *  
p1=Person('ahmed',
          [[1,2],[3,5],[7,8],[5,2]]
          ,[1,4,2,5],5) # code 5 nouveau person 
p2=Person('ahmed',
          [[5,7],[2,4],[1,8]],
          [1]) #code 1 valeur par defaut
p3=Person('ahmed',
          [[8,5]],
          [3]) #code 2 valeur par defaut


taille_IAGI=4
relation_p_class=graphe(taille_IAGI)

relation_p_class.add_ele(p1,False)    
relation_p_class.add_ele(p2,True)
relation_p_class.add_ele(p3,True) 

matrix=relation_p_class.get_matrix()
print(matrix['mat_amis'])
            