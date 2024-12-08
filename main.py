import tkinter as tk
from tkinter import messagebox
from tree.node import node

from recherche_profondeur.profondeur import print_profondeur_path
from A_star.a_star_algo import display_A_star_path
from recherche_largeur.bfs import run_bfs
from constants import *

import sys
# Constants


# A* and Dijkstra GUI
class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Visualization")

        # Initialize grid
        self.start = (0, 0)
        self.end = (GRID_SIZE - 1, GRID_SIZE - 1)
        self.grid = [[{"canva":0,"distance":self.calcul_distance((r,c),self.end)} for r in range(GRID_SIZE)] for c in range(GRID_SIZE)]
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack()
        
        # Canvas
       # Label and input for "Name"
        """
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        tk.Label(self.frame, text="Vitesse:").pack(side="left", padx=5)
        self.entry_speed = tk.Entry(self.frame, width=10, textvariable=ANIMATION_SPEED)
        self.entry_speed.pack(side="left", padx=5)
        self.entry_speed.insert(0, str(ANIMATION_SPEED))
        # Label and Entry for "Age"
        tk.Label(self.frame, text="Dimension:").pack(side="left", padx=5)
        self.entry_dim = tk.Entry(self.frame, width=5)
        self.entry_dim.pack(side="left", padx=5)
        self.entry_dim.insert(0, str(GRID_SIZE))

        # Button to trigger input retrieval
        self.button = tk.Button(root, text="enter", command=self.update_matrix())
        self.button.pack(pady=10)
        """

        self.create_grid()
        self.path_lines=[]
        # Mouse bindings
        self.canvas.bind("<B1-Motion>", self.add_obstacle)
        self.canvas.bind("<Button-1>", self.add_obstacle)
        self.canvas.bind("<Button-3>", self.set_start_or_end)
        
        # Buttons
        self.a_star_button = tk.Button(self.root, text="A*", command=lambda: display_A_star_path(self,self.start))
        self.a_star_button.pack(side="left")
        self.profondeur_button = tk.Button(self.root, text="recherche en profondeur", command=lambda:print_profondeur_path(self))
        self.profondeur_button.pack(side="left")
        self.largeur_button = tk.Button(self.root, text="recherche en largeur", command=lambda:run_bfs(self) )
        self.largeur_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side="left")

    def update_matrix(self):
        ANIMATION_SPEED=int(self.entry_speed.get())
        GRID_SIZE=int(self.entry_dim.get())
        print(ANIMATION_SPEED)
        self.grid = [[{"canva":0,"distance":self.calcul_distance((r,c),self.end)} for r in range(GRID_SIZE)] for c in range(GRID_SIZE)]
        self.create_grid()
        

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
                self.grid[row][col]["distance"] =self.calcul_distance((row,col),self.end)

    def visited_coloring(self, node):
        if (node.get_data()[0],node.get_data()[1]) != self.start and (node.get_data()[0],node.get_data()[1])  != self.end:
            self.canvas.itemconfig(app.grid[node.get_data()[0]][node.get_data()[1]]["canva"], fill=VISITED_COLOR)
            self.root.update()
            self.root.after(ANIMATION_SPEED)

    def set_start_or_end(self, event):
        """Set start or end point."""
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (row, col) != self.start and (row, col) != self.end and self.canvas.itemcget(self.grid[row][col]["canva"], "fill") != OBSTACLE_COLOR:
            if self.start == (row, col):
                self.start = self.end
                self.end = (row, col)
            else:
                self.end = (row, col)
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.grid[i][j]["distance"] != -1:
                        self.grid[i][j]["distance"] =self.calcul_distance((i,j),self.end)
            self.reset_grid()

    def remove_previous_pattern(self):  
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col]["distance"] != -1 and (row, col) != self.start and (row, col) != self.end:
                    self.canvas.itemconfig(self.grid[row][col]["canva"], fill=EMPTY_COLOR)
                    self.grid[row][col]["distance"] = self.calcul_distance((row,col),self.end)
         #effacer le lignes
        for line in self.path_lines:
            self.canvas.delete(line)
        self.path_lines.clear()
    def reset_grid(self):
        """Reset the grid to its initial state."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = START_COLOR if (row, col) == self.start else END_COLOR if (row, col) == self.end else EMPTY_COLOR
                self.canvas.itemconfig(self.grid[row][col]["canva"], fill=color)
                self.grid[row][col]["distance"] = self.calcul_distance((row,col),self.end)
        #effacer le lignes
        for line in self.path_lines:
            self.canvas.delete(line)
        self.path_lines.clear()

    def draw_path_line(self,path):
        for i in range(len(path) - 1):
            x1, y1 = path[i][1] * CELL_SIZE + CELL_SIZE // 2, path[i][0] * CELL_SIZE + CELL_SIZE // 2
            x2, y2 = path[i + 1][1] * CELL_SIZE + CELL_SIZE // 2, path[i + 1][0] * CELL_SIZE + CELL_SIZE // 2
            line_id=self.canvas.create_line(x1, y1, x2, y2, fill=PATH_COLOR, width=2)
            self.path_lines.append(line_id)

    def calcul_distance(self,a,b):
        return abs(a[0]-b[0])+abs(a[1]-b[1])

# Run the application
if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)

    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
    
