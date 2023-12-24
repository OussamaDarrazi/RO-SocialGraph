from classes_project import *  

p1=Person('ibrahim goumrane',
          [[1,2],[3,5],[7,8],[5,2]]
          ,[1,4,2],5)     # code 5 nouveau person
p2=Person('ismail moufatih',
          [[5,7],[2,4],[1,8]],
          )                 #code 1 valeur par defaut
p3=Person('oussama darrazi',
          [[8,5]],
          )                 #code 2 valeur par defaut
p4=Person('mohsine mohsine',
          [[8,5]],
          )                 #code 3 valeur par defaut
p5=Person('yassin ahmed',
          [[8,4]],
          ) #code 3 valeur par defaut
taille_IAGI=4 # nombre d'etudiant 4
relation_p_class=graphe(taille_IAGI)

relation_p_class.add_ele(p1,False)    #nombre d'etudiant devient 5 parceque il n'est pas exsistant au prealable
relation_p_class.add_ele(p2,True)
relation_p_class.add_ele(p3,True)

matrix=relation_p_class.get_matrix() 
title=f"Graph des amis de {p1.nom}"


# afficher les amis pour une personnes specific

affichage_amis(p2,matrix,title)   


# suggeger des amis pour une persone dans notre cas c'est ismail             
suggestin_friend_based_current_friend(p2,relation_p_class)








 