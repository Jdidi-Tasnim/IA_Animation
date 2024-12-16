from constants import *
from tree.node import node
from tkinter import messagebox
import time

def node_equal_to(node1,node2):
    if (node1.get_data()[0],node1.get_data()[1])==(node2.get_data()[0],node2.get_data()[1]):
        return True
    return False
def recherche_A_star(app, initial_node_cords):
    #initialiser le noeud de départ
    initial_node=node(initial_node_cords+(0,),None)
    #ajouter le noeud de départ à la liste ouverte
    open_list=[initial_node]
    closed_list=[]
    n_visited=0
    #parcourir la liste ouverte jusqu'à ce qu'elle soit vide
    while len(open_list)>0:
        current_node=open_list[0]
        open_list.remove(current_node)
        closed_list.append(current_node)
        app.visited_coloring(current_node)
        n_visited+=1

        #si oon atteint le point d'arrivée on va retourner True et le noeud actuel et on arrête la recherche
        if (current_node.get_data()[0],current_node.get_data()[1])==app.end:
            return True,current_node,n_visited-1
        #on va parcourir les directions possibles (haut, bas, gauche, droite)(les voisins)
        for direction in DIRECTIONS:
            #vérifier si le voisin est dans les limites de la grille , n'est pas un obstacle et n'est pas déjà visité
            if current_node.get_data()[0]+direction[0]<0 or current_node.get_data()[1]+direction[1]<0 or current_node.get_data()[0]+direction[0]>=GRID_SIZE or current_node.get_data()[1]+direction[1]>=GRID_SIZE or app.grid[current_node.get_data()[0]+direction[0]][current_node.get_data()[1]+direction[1]]["distance"] == -1:
                continue
            #créer un nouveau noeud pour le voisin valide
            next_node=node((current_node.get_data()[0]+direction[0],current_node.get_data()[1]+direction[1],current_node.get_data()[2]+1),current_node)
            current_node.add_child(next_node)
            #si le voisin est déjà visité, on vérifie si on peut améliorer le chemin
            for n in closed_list:
                if node_equal_to(n,next_node):
                    if n.get_data()[2]>next_node.get_data()[2]:
                        appended=True
                        closed_list.remove(n)
                        open_list.append(next_node)
                    break
            else:
                #si le voisin n'est pas visité mais dans la liste ouverte, on vérifie si on peut améliorer le chemin
                for n in open_list:
                    if node_equal_to(n,next_node):
                        if n.get_data()[2]>next_node.get_data()[2]:
                            open_list.remove(n)
                            open_list.append(next_node)

                        break
                else:
                    #si le voisin n'est pas visité, on l'ajoute à la liste ouverte
                    open_list.append(next_node)
                    #on trie la liste ouverte selon la distance et le coût
        open_list.sort(key=lambda x:x.get_data()[2]+app.grid[x.get_data()[0]][x.get_data()[1]]["distance"])
    return False,None,n_visited
#fonction pour afficher le chemin trouvé par A*
def get_path_a_star(app,actual_node):
    path=[]
    while actual_node.get_data()!=app.start+(0,):
        path.append(actual_node.get_data())
        actual_node=actual_node.get_parent()
    path.append(app.start)
    return path

#fonction pour implémenter A* 
def display_A_star_path(app,init_cords):
    app.remove_previous_pattern()
    t1=time.time()
    result,last_node,n=recherche_A_star(app,init_cords)
    t2=time.time()
    if result:
        path=last_node.get_path(app)
        app.draw_path_line(path)
        print("=================    A*    ================")
        print("Path found, using A*, in",t2-t1,"seconds.")
        print("N° of nodes visited:",n)
        print("longueur du chemin :",len(path))

    else :
        messagebox.showinfo("No Path", "No path found to the destination.")
