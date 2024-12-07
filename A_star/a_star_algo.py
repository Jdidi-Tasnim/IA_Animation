from constants import *
from tree.node import node


def node_equal_to(node1,node2):
    if (node1.get_data()[0],node1.get_data()[1])==n(node.get_data()[0],node2.get_data()[1]):
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
        if current_node.get_data() == app.end:
            return True,current_node
        for direction in DIRECTIONS:
            if current_node.get_data()[0]+direction[0]<0 or current_node.get_data()[1]+direction[1]<0 or current_node.get_data()[0]+direction[0]>=GRID_SIZE or current_node.get_data()[1]+direction[1]>=GRID_SIZE or app.grid[current_node.get_data()[0]+direction[0]][current_node.get_data()[1]+direction[1]]["distance"] == -1:
                continue
            next_node=node((current_node.get_data()[0]+direction[0],current_node.get_data()[1]+direction[1],current_node.get_data()[2]+1),current_node)
            # vérifier avec le cours 
            for n in close:
                if node_equal_to(n,next_node):
                    if n.get_data()[2]>next_node.get_data()[2]:
                        n.set_parent(next_node.get_parent())
                    break
                continue
            for node in opent:
                if node.get_data() == next_node.get_data():
                    if node.get_data()[0]+node.get_data()[1]>next_node.get_data()[0]+next_node.get_data()[1]:
                        node.set_parent(next_node.get_parent())
                    break
            else:
                opent.append(next_node)