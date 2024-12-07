import tkinter as tk
from collections import deque
from tkinter import messagebox
import time  # To add delays for smoother animation

CELL_SIZE = 20  # Size of each cell in pixels
GRID_SIZE = 20  # Size of the grid

# Colors for visualization
START_COLOR = "green"
END_COLOR = "red"
PATH_COLOR = "yellow"
VISITED_COLOR = "purple"
OBSTACLE_COLOR = "black"
EMPTY_COLOR = "white"

# Directions for neighbor cells (up, down, left, right)
DIRECTIONS = [
    (0, 1),   # Right
    (1, 0),   # Down
    (0, -1),  # Left
    (-1, 0)   # Up
]

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Breadth-First Search Visualization")

        # Canvas setup
        self.canvas = tk.Canvas(
            self.root,
            width=GRID_SIZE * CELL_SIZE,
            height=GRID_SIZE * CELL_SIZE
        )
        self.canvas.pack()

        # Initialize grid cells with properties
        # Each cell has a canvas rectangle and a distance value
        self.grid = [
            [{"canva": None, "distance": 0} for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]
        self.start = (0, 0)  # Starting point
        self.end = (GRID_SIZE - 1, GRID_SIZE - 1)  # Ending point

        self.create_grid()

        # Mouse and keyboard bindings
        self.canvas.bind("<Button-1>", self.toggle_obstacle)  # Left click to toggle obstacles
        self.canvas.bind("<Button-3>", self.set_start_or_end)  # Right click to set start or end point
        self.root.bind("<space>", lambda event: run_bfs(self))  # Press space to start BFS

        self.largeur_button = tk.Button(self.root, text="recherche en largeur", command=lambda: run_bfs(self))
        self.largeur_button.pack(side="left")

    def create_grid(self):
        """Initialize the grid of cells."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x1 = col * CELL_SIZE  # Top-left x-coordinate
                y1 = row * CELL_SIZE  # Top-left y-coordinate
                x2 = x1 + CELL_SIZE   # Bottom-right x-coordinate
                y2 = y1 + CELL_SIZE   # Bottom-right y-coordinate

                # Set initial color based on start and end points
                if (row, col) == self.start:
                    color = START_COLOR
                elif (row, col) == self.end:
                    color = END_COLOR
                else:
                    color = EMPTY_COLOR

                # Create the cell rectangle on the canvas
                cell = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="gray"
                )
                # Store the canvas rectangle and initial distance value
                self.grid[row][col]["canva"] = cell
                self.grid[row][col]["distance"] = 0  # Initialize distance

    def toggle_obstacle(self, event):
        """Toggle obstacle cells on left mouse click."""
        row = event.y // CELL_SIZE  # Get the row index
        col = event.x // CELL_SIZE  # Get the column index

        # Ensure coordinates are within grid bounds
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            # Do not change the start or end cell
            if (row, col) != self.start and (row, col) != self.end:
                current_color = self.canvas.itemcget(
                    self.grid[row][col]["canva"], "fill"
                )
                if current_color != OBSTACLE_COLOR:
                    # Set cell as obstacle
                    self.canvas.itemconfig(
                        self.grid[row][col]["canva"], fill=OBSTACLE_COLOR
                    )
                    self.grid[row][col]["distance"] = -1  # Mark as obstacle
                else:
                    # Remove obstacle
                    self.canvas.itemconfig(
                        self.grid[row][col]["canva"], fill=EMPTY_COLOR
                    )
                    self.grid[row][col]["distance"] = 0  # Reset distance

    def set_start_or_end(self, event):
        """Set the start or end point on right mouse click."""
        row = event.y // CELL_SIZE  # Get the row index
        col = event.x // CELL_SIZE  # Get the column index

        # Ensure coordinates are within grid bounds
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            cell_color = self.canvas.itemcget(
                self.grid[row][col]["canva"], "fill"
            )
            # Do not set on obstacle cells
            if cell_color != OBSTACLE_COLOR:
                if (row, col) == self.start or (row, col) == self.end:
                    return  # Do nothing if clicking on the start or end point
                else:
                    # Decide whether to set start or end point
                    if self.start == (0, 0):
                        # Reset previous start cell
                        self.canvas.itemconfig(
                            self.grid[self.start[0]][self.start[1]]["canva"],
                            fill=EMPTY_COLOR
                        )
                        # Set new start point
                        self.start = (row, col)
                        self.canvas.itemconfig(
                            self.grid[row][col]["canva"], fill=START_COLOR
                        )
                    else:
                        # Reset previous end cell
                        self.canvas.itemconfig(
                            self.grid[self.end[0]][self.end[1]]["canva"],
                            fill=EMPTY_COLOR
                        )
                        # Set new end point
                        self.end = (row, col)
                        self.canvas.itemconfig(
                            self.grid[row][col]["canva"], fill=END_COLOR
                        )

def run_bfs(app):
    """Perform Breadth-First Search from start to end with animation."""
    # Clear previous paths and visited cells
    clear_search(app)

    queue = deque()
    queue.append(app.start)
    visited = set()
    visited.add(app.start)
    parent = {}  # To reconstruct the path

    while queue:
        current = queue.popleft()

        if current == app.end:
            break  # Path found to the end point

        for direction in DIRECTIONS:
            neighbor_row = current[0] + direction[0]
            neighbor_col = current[1] + direction[1]
            neighbor = (neighbor_row, neighbor_col)

            # Check if neighbor is within grid bounds
            if 0 <= neighbor_row < GRID_SIZE and 0 <= neighbor_col < GRID_SIZE:
                # Check if neighbor is not visited and not an obstacle
                if neighbor not in visited and app.grid[neighbor_row][neighbor_col]["distance"] != -1:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parent[neighbor] = current  # Keep track of the path
                    # Visualize visited cells
                    if neighbor != app.end:
                        app.canvas.itemconfig(
                            app.grid[neighbor_row][neighbor_col]["canva"],
                            fill=VISITED_COLOR
                        )
                    app.root.update()  # Update the GUI
                    time.sleep(0.02)    # Pause for animation effect

    # Reconstruct and visualize the path from end to start
    current = app.end
    if current in parent or current == app.start:
        while current != app.start:
            current = parent.get(current)
            if current and current != app.start:
                app.canvas.itemconfig(
                    app.grid[current[0]][current[1]]["canva"],
                    fill=PATH_COLOR
                )
                app.root.update()  # Update the GUI
                time.sleep(0.02)    # Pause for animation effect
    else:
        # No path found
        messagebox.showinfo("No Path", "No path found to the destination.")

def clear_search(app):
    """Clear the visualization of the search."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            current_color = app.canvas.itemcget(app.grid[row][col]["canva"], "fill")
            if current_color in (VISITED_COLOR, PATH_COLOR):
                if (row, col) == app.start:
                    app.canvas.itemconfig(app.grid[row][col]["canva"], fill=START_COLOR)
                elif (row, col) == app.end:
                    app.canvas.itemconfig(app.grid[row][col]["canva"], fill=END_COLOR)
                else:
                    app.canvas.itemconfig(app.grid[row][col]["canva"], fill=EMPTY_COLOR)
    app.root.update()  # Update the GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()
