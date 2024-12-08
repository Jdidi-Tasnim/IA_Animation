from constants import *
from tree.node import node


def node_equal_to(node1,node2):
    if (node1.get_data()[0],node1.get_data()[1])==(node2.get_data()[0],node2.get_data()[1]):
        return True
    return False
def recherche_A_star(app, initial_node_cords):
    initial_node=node(initial_node_cords+(0,),None)
    opent=[initial_node]
    close=[]
    
    while len(opent)>0:
        current_node=opent[0]
        opent.remove(current_node)
        close.append(current_node)
        app.visited_coloring(current_node)
        if (current_node.get_data()[0],current_node.get_data()[1])==app.end:
            return True,current_node
        for direction in DIRECTIONS:
            
            if current_node.get_data()[0]+direction[0]<0 or current_node.get_data()[1]+direction[1]<0 or current_node.get_data()[0]+direction[0]>=GRID_SIZE or current_node.get_data()[1]+direction[1]>=GRID_SIZE or app.grid[current_node.get_data()[0]+direction[0]][current_node.get_data()[1]+direction[1]]["distance"] == -1:
                continue
            next_node=node((current_node.get_data()[0]+direction[0],current_node.get_data()[1]+direction[1],current_node.get_data()[2]+1),current_node)
            # vérifier avec le cours 

            for n in close:
                if node_equal_to(n,next_node):
                    if n.get_data()[2]>next_node.get_data()[2]:
                        appended=True
                        close.remove(n)
                        opent.append(next_node)
                    break
            else:
                for n in opent:
                    if node_equal_to(n,next_node):
                        if n.get_data()[2]>next_node.get_data()[2]:
                            opent.remove(n)
                            opent.append(next_node)

                        break
                else:
                    opent.append(next_node)
        opent.sort(key=lambda x:x.get_data()[2]+app.grid[x.get_data()[0]][x.get_data()[1]]["distance"])
    return False,None

def get_path_a_star(app,actual_node):
    path=[]
    while actual_node.get_data()!=app.start+(0,):
        path.append(actual_node.get_data())
        actual_node=actual_node.get_parent()
    path.append(app.start)
    return path

def display_A_star_path(app,init_cords):

    result,last_node=recherche_A_star(app,init_cords)
    if result:
        path=path=last_node.get_path(app)
        app.draw_path_line(path)
        return True