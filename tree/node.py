
class node :


    def __init__(self,data,parent):
        self.data=data
        self.children=[]
        self.parent=parent
    
    def add_child(self,child):
        self.children.append(child)
        child.parent=self
    def remove_child(self,child):
        self.children.remove(child)
        child.parent=None
    def get_children(self):
        return self.children
    def get_parent(self):
        return self.parent
    def get_data(self):
        return self.data
    def set_data(self,data):
        self.data=data
    def set_parent(self,parent):
        self.parent=parent
    def get_all_children(self):
        children=[]
        for child in self.children:
            children.append(child)
            children+=child.get_all_children()
        return children
    def get_all_children_data(self):
        children=[]
        for child in self.children:
            children.append(child.get_data())
            children+=child.get_all_children_data()
        return children
    def get_leaf(self):
        leafs=[]
        if len(self.children)==0:
            return self
        else:
            for child in self.children:
                leafs.append(child.get_leaf())
        return leafs
    def get_path(self,app):
        path=[]
        actual_node=self
        while (actual_node.get_data()[0],actual_node.get_data()[1]) !=app.start:
            path.append(actual_node.get_data())
            actual_node=actual_node.get_parent()
        path.append(app.start)
        return path