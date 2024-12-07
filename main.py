import tkinter as tk
from queue import PriorityQueue

# Constants
GRID_SIZE = 20  # Number of cells per row/column
CELL_SIZE = 20  # Cell size in pixels
START_COLOR = "green"
END_COLOR = "red"
PATH_COLOR = "yellow"
VISITED_COLOR = "purple"
OBSTACLE_COLOR = "black"
EMPTY_COLOR = "white"

# Directions for neighbors
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

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
        self.profondeur_button = tk.Button(self.root, text="recherche en profondeur", command=lambda:print("") )
        self.profondeur_button.pack(side="left")
        self.largeur_button = tk.Button(self.root, text="recherche en largeur", command=lambda:print("") )
        self.largeur_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_grid)
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

    def reset_grid(self):
        """Reset the grid to its initial state."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = START_COLOR if (row, col) == self.start else END_COLOR if (row, col) == self.end else EMPTY_COLOR
                self.canvas.itemconfig(self.grid[row][col]["canva"], fill=color)
                self.grid[row][col]["distance"] = row + col
    

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
