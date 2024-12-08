#on va utiliser deque (double-ended queue) pour la file d'attente
from collections import deque
#on va importer les constantes et les directions
from constants import *
#on va importer le temps pour insérer des pauses (animation)
import time
#on va importer le noeud pour créer un objet noeud
from tree.node import node
#on va importer le messagebox pour afficher un message d'erreur pour notifier l'utilisateur exemple: pas de chemin trouvé
from tkinter import messagebox
#une fonction pour exécuter la recherche en largeur pour trouver le chemin le plus court
def run_bfs(app):
    """Perform Breadth-First Search from start to end with animation."""
   
    #app l'objet qui contient les informations de l'interface graphique (position de départ, position d'arrivée, grille, canvas)
    # remove pour supprimer les anciens chemins et les cellules visitées
    app.remove_previous_pattern()
    #on va créer une file d'attente pour les noeuds à visiter (FIFO)
    t1 = time.time()
    queue = deque()
    #on va ajouter le noeud de départ à la file d'attente
    queue.append(app.start)
    # visited pour garder les noeuds visités
    visited = set()
    #on va ajouter le noeud de départ à la liste des noeuds visités immédiatement
    visited.add(app.start)
    #on va créer un dictionnaire pour garder le parent de chaque noeud visitée pour reconstruire le chemin
    parent = {}  # To reconstruct the path
#parcourir la file d'attente jusqu'à ce qu'elle soit vide
    while queue:
        #on va récupérer le premier élément de la file d'attente (couche par couche "pronfondeur uniforme")
        current = queue.popleft()
# si cellular est le noeud d'arrivée on va sortir de la boucle
        if current == app.end:
            break  # Path found to the end point
# on va parcourir les directions possibles (haut, bas, gauche, droite) (explorer les voisins)
        for direction in DIRECTIONS:
            neighbor_row = current[0] + direction[0]
            neighbor_col = current[1] + direction[1]
            neighbor = (neighbor_row, neighbor_col)

            #vérifier si le voisin est dans les limites de la grille
            if 0 <= neighbor_row < GRID_SIZE and 0 <= neighbor_col < GRID_SIZE:
                #vérifier si le voisin n'est pas un obstacle et n'est pas déjà visité
                if neighbor not in visited and app.grid[neighbor_row][neighbor_col]["distance"] != -1:
                 #on l'ajoute à la file d'attente et on le marque comme visité
                    queue.append(neighbor)
                    visited.add(neighbor)
                    #on va garder le parent du voisin pour reconstruire le chemin
                    parent[neighbor] = current  
                    #colorier le voisin en visité 
                    app.visited_coloring(node((neighbor_row,neighbor_col)))    # Pause for animation effect

    # si le point d'arrivée présent dans parent ou c'est le point de départ on va reconstruire le chemin
    t2 = time.time()
    current = app.end
    if current in parent or current == app.start:
        #remontée depuis point d'arrivée jusqu'au point de départ en ajoutant à chaque fois chaque cellule visitée
        path=[]
        while current != app.start:
            path.append(current)
            current = parent.get(current)
             #ajouter le point de départ au chemin
        path.append(app.start)
        app.draw_path_line(path)

        print("=================    BFS    ================")
        print("Path found, using BFS, in",t2-t1,"seconds.")
        print("N° of nodes visited:",len(visited)-1)
    else:
        # SION on affiche un message d'erreur
        messagebox.showinfo("No Path", "No path found to the destination.")
