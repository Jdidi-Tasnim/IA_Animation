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
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.start = (0, 0)
        self.end = (GRID_SIZE - 1, GRID_SIZE - 1)
        self.create_grid()

        # Mouse bindings
        self.canvas.bind("<Button-1>", self.add_obstacle)
        self.canvas.bind("<Button-3>", self.set_start_or_end)

        # Buttons
        self.a_star_button = tk.Button(self.root, text="A*", command=lambda: self.run_algorithm(self.a_star))
        self.a_star_button.pack(side="left")
        self.dijkstra_button = tk.Button(self.root, text="Dijkstra", command=lambda: self.run_algorithm(self.dijkstra))
        self.dijkstra_button.pack(side="left")
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side="left")

    def create_grid(self):
        """Draw grid on canvas."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = START_COLOR if (row, col) == self.start else END_COLOR if (row, col) == self.end else EMPTY_COLOR
                self.grid[row][col] = self.canvas.create_rectangle(
                    col * CELL_SIZE, row * CELL_SIZE, 
                    (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE, 
                    fill=color, outline="gray"
                )

    def add_obstacle(self, event):
        """Add an obstacle to the grid."""
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (row, col) != self.start and (row, col) != self.end:
            self.canvas.itemconfig(self.grid[row][col], fill=OBSTACLE_COLOR)

    def set_start_or_end(self, event):
        """Set start or end point."""
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if (row, col) != self.start and (row, col) != self.end and self.canvas.itemcget(self.grid[row][col], "fill") != OBSTACLE_COLOR:
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
                self.canvas.itemconfig(self.grid[row][col], fill=color)

    def neighbors(self, row, col):
        """Get valid neighbors."""
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and self.canvas.itemcget(self.grid[r][c], "fill") != OBSTACLE_COLOR:
                yield r, c

    def heuristic(self, a, b):
        """Heuristic for A*."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def run_algorithm(self, algorithm):
        """Run the selected algorithm."""
        self.reset_grid()
        path, visited = algorithm()
        for row, col in visited:
            if (row, col) != self.start and (row, col) != self.end:
                self.canvas.itemconfig(self.grid[row][col], fill=VISITED_COLOR)
        for row, col in path:
            if (row, col) != self.start and (row, col) != self.end:
                self.canvas.itemconfig(self.grid[row][col], fill=PATH_COLOR)

    def a_star(self):
        """A* algorithm."""
        open_set = PriorityQueue()
        open_set.put((0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end)}
        visited = set()

        while not open_set.empty():
            _, current = open_set.get()
            visited.add(current)

            if current == self.end:
                return self.reconstruct_path(came_from, current), visited

            for neighbor in self.neighbors(*current):
                temp_g_score = g_score[current] + 1

                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, self.end)
                    open_set.put((f_score[neighbor], neighbor))

        return [], visited


    def reconstruct_path(self, came_from, current):
        """Reconstruct path from end to start."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
