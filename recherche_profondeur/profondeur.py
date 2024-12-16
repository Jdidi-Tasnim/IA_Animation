#node pour présenter un noeud dans l'arbre
from tree.node import node
from constants import *
import time
from tkinter import messagebox
#fonction pour la recherche en profondeur
#app l'objet qui contient les informations de l'interface graphique (position de départ, position d'arrivée, grille, canvas)
#actual_node le noeud actuel
#root le noeud racine
def recherche_en_profondeur(app, actual_node,root=node((0,0),None)):
    #¢ette partie est optimizable normalement
    #recupére tous les enfants du noeud racine
    visited_nodes=root.get_all_children_data()
    #ajoute le noeud actuel à la liste des noeuds visités
    visited_nodes.append(root.get_data())
    #si le noeud actuel n'est pas le point de départ ou le point d'arrivée on va le colorier
    if actual_node.get_data() != app.start and actual_node.get_data() != app.end:
      app.visited_coloring(actual_node)
    #si le noeud actuel est le point d'arrivée on va retourner True et le noeud actuel
    if actual_node.get_data() == app.end:
        return True,actual_node
    #on va parcourir les directions possibles (haut, bas, gauche, droite)(les voisins)
    for direction in DIRECTIONS:
        #vérifier si le voisin est dans les limites de la grille , n'est pas un obstacle et n'est pas déjà visité
        if actual_node.get_data()[0]+direction[0]<0 or actual_node.get_data()[1]+direction[1]<0 or actual_node.get_data()[0]+direction[0]>=GRID_SIZE or actual_node.get_data()[1]+direction[1]>=GRID_SIZE or app.grid[actual_node.get_data()[0]+direction[0]][actual_node.get_data()[1]+direction[1]]["distance"] == -1 or (actual_node.get_data()[0]+direction[0],actual_node.get_data()[1]+direction[1]) in visited_nodes:
            continue
        #créer un nouveau noeud pour le voisin valide
        next_node=node((actual_node.get_data()[0]+direction[0],actual_node.get_data()[1]+direction[1]),actual_node)
       #ajouter le voisin comme enfant du noeud actuel
        actual_node.add_child(next_node)
        #appeler la fonction récursivement 
        result,last_node=recherche_en_profondeur(app,next_node,root)
        if result:
            #si le chemin est trouvé on va retourner True et le noeud actuel
            return True,last_node
        # si tous les voisins sont vistés et aucun chemin trouvé on rettourne false
    return False,None

def print_profondeur_path(app):
    #on efface les anciens chemins ou noeuds visitées de grille
    app.remove_previous_pattern()
    root_node=node((0,0),None)
    #on démarrer le chronomètre
    t1=time.time()
    #on appelle la fonction de recherche en profondeur
    result,last_node=recherche_en_profondeur(app,root_node,root_node)
    #enrigistrer le temps final
    t2=time.time()
    #si le chemin est trouvé on va le dessiner
    if result:
        path=last_node.get_path(app)
        app.draw_path_line(path)
        print("=================    DFS    ================")
        print("Path found, using DFS, in",t2-t1,"seconds.")
        print("N° of nodes visited:",len(root_node.get_all_children_data()))
        print("longueur du chemin :",len(path))    
        #sinon on affiche un message d'erreur
    else:
        messagebox.showinfo("No Path", "No path found to the destination.")