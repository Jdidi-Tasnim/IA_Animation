from tree.node import node
from constants import *
def recherche_en_profondeur(app, actual_node,root=node((0,0),None)):
      #cette partie est optimizable normalement
      visited_nodes=root.get_all_children_data()
      visited_nodes.append(root.get_data())
      if actual_node.get_data() != app.start and actual_node.get_data() != app.end:
          app.canvas.itemconfig(app.grid[actual_node.get_data()[0]][actual_node.get_data()[1]]["canva"], fill=VISITED_COLOR)
      #
      if actual_node.get_data() == app.end:
          return True,actual_node
      for direction in DIRECTIONS:
          if actual_node.get_data()[0]+direction[0]<0 or actual_node.get_data()[1]+direction[1]<0 or actual_node.get_data()[0]+direction[0]>=GRID_SIZE or actual_node.get_data()[1]+direction[1]>=GRID_SIZE or app.grid[actual_node.get_data()[0]+direction[0]][actual_node.get_data()[1]+direction[1]]["distance"] == -1 or (actual_node.get_data()[0]+direction[0],actual_node.get_data()[1]+direction[1]) in visited_nodes:
              continue
          next_node=node((actual_node.get_data()[0]+direction[0],actual_node.get_data()[1]+direction[1]),actual_node)
          actual_node.add_child(next_node)
          result,last_node=recherche_en_profondeur(app,next_node,root)
          if result:
              return True,last_node
      return False,None
def get_path_profondeur(app,actual_node):
    path=[]
    while actual_node.get_data()!=app.start:
        path.append(actual_node.get_data())
        actual_node=actual_node.get_parent()
    path.append(app.start)
    return path

def print_profondeur_path(app):
    root_node=node((0,0),None)
    result,last_node=recherche_en_profondeur(app,root_node,root_node)
    path=get_path_profondeur(app,last_node)
    for i in path:
        if i!=app.start and i!=app.end:
            app.canvas.itemconfig(app.grid[i[0]][i[1]]["canva"], fill=PATH_COLOR)