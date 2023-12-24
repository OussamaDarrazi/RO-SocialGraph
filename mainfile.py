from classes_project import *  
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
p1=Person('ibrahim\n goumrane',
          [[1,2],[3,5],[7,8],[5,2]]
          ,[1,4,2,5],5)     # code 5 nouveau person
p2=Person('ismail \nmoufatih',
          [[5,7],[2,4],[1,8]],
          )                 #code 1 valeur par defaut
p3=Person('oussama \ndarrazi',
          [[8,5]],
          )                 #code 2 valeur par defaut
p4=Person('mohsine \nmohsine',
          [[8,5]],
          )                 #code 3 valeur par defaut
p5=Person('yassin\n ahmed',
          [[8,4]],
          ) #code 3 valeur par defaut
taille_IAGI=4 # nombre d'etudiant 4
relation_p_class=graphe(taille_IAGI)

relation_p_class.add_ele(p1,False)    #nombre d'etudiant devient 5 parceque il n'est pas exsistant au prealable
relation_p_class.add_ele(p2,True)
relation_p_class.add_ele(p3,True)

matrix=relation_p_class.get_matrix() 

def affichage_amis(p1):
    #ajout de titre
    plt.title(f"Graph des amis de {p1.nom}")
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
affichage_amis(p2)    