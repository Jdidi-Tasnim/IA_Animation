from tree.node import node
from constants import *
import time
def recherche_en_profondeur(app, actual_node,root=node((0,0),None)):
      #cette partie est optimizable normalement
      visited_nodes=root.get_all_children_data()
      visited_nodes.append(root.get_data())
      if actual_node.get_data() != app.start and actual_node.get_data() != app.end:
        app.visited_coloring(actual_node)
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

def print_profondeur_path(app):
    root_node=node((0,0),None)
    result,last_node=recherche_en_profondeur(app,root_node,root_node)
    path=last_node.get_path(app)
    app.draw_path_line(path)