import tkinter as tk
from queue import PriorityQueue
from tree.node import node
import time
from recherche_profondeur.profondeur import print_profondeur_path
from constants import *
# Constants


# A* and Dijkstra GUI
class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Visualization")

        # Canvas
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()

        # Initialize grid
        self.grid = [[{"canva":0,"distance":r+c} for r in range(GRID_SIZE)] for c in range(GRID_SIZE)]
        self.start = (0, 0)
        self.end = (GRID_SIZE - 1, GRID_SIZE - 1)

        self.create_grid()

        # Mouse bindings
        self.canvas.bind("<Button-1>", self.add_obstacle)
        self.canvas.bind("<Button-3>", self.set_start_or_end)
        
        # Buttons
        self.a_star_button = tk.Button(self.root, text="A*", command=lambda: print("a*"))
        self.a_star_button.pack(side="left")
        self.profondeur_button = tk.Button(self.root, text="recherche en profondeur", command=lambda:print_profondeur_path(self))
        self.profondeur_button.pack(side="left")
        self.largeur_button = tk.Button(self.root, text="recherche en largeur", command=lambda:print("") )
        self.largeur_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.remove_previous_pattern)
        self.reset_button.pack(side="left")
    def create_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = START_COLOR if (row, col) == self.start else END_COLOR if (row, col) == self.end else EMPTY_COLOR
                self.grid[row][col]["canva"] = self.canvas.create_rectangle(
                    col * CELL_SIZE, row * CELL_SIZE, 
                    (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE, 
                    fill=color, outline="gray"
                )
    def add_obstacle(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE

        if self.grid[row][col]["distance"] != -1:
            if (row, col) != self.start and (row, col) != self.end:
                self.canvas.itemconfig(self.grid[row][col]["canva"], fill=OBSTACLE_COLOR)
                self.grid[row][col]["distance"] = -1
        else :
            if (row, col) != self.start and (row, col) != self.end:
                self.canvas.itemconfig(self.grid[row][col]["canva"], fill=EMPTY_COLOR)
                self.grid[row][col]["distance"] = row + col

    def set_start_or_end(self, event):
        """Set start or end point."""
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (row, col) != self.start and (row, col) != self.end and self.canvas.itemcget(self.grid[row][col]["canva"], "fill") != OBSTACLE_COLOR:
            if self.start == (row, col):
                self.start = self.end
                self.end = (row, col)
            else:
                self.end = (row, col)
            self.reset_grid()

    def remove_previous_pattern(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col]["distance"] != -1 and (row, col) != self.start and (row, col) != self.end:
                    self.canvas.itemconfig(self.grid[row][col]["canva"], fill=EMPTY_COLOR)
                    self.grid[row][col]["distance"] = row + col
    def reset_grid(self):
        """Reset the grid to its initial state."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = START_COLOR if (row, col) == self.start else END_COLOR if (row, col) == self.end else EMPTY_COLOR
                self.canvas.itemconfig(self.grid[row][col]["canva"], fill=color)
                self.grid[row][col]["distance"] = row + col
    

# Run the application
if __name__ == "__main__":
    root = node((0,0),None)
    root.add_child(node((0,1),root))
    root.add_child(node((1,0),root))
    root.add_child(node((1,1),root))
    print(root.get_all_children_data())
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
    
