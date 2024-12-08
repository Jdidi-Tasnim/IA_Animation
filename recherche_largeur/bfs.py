from collections import deque
from constants import *
import time
from tree.node import node
from tkinter import messagebox

def run_bfs(app):
    """Perform Breadth-First Search from start to end with animation."""
    # Clear previous paths and visited cells
    app.remove_previous_pattern()
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
                    app.visited_coloring(node((neighbor_row,neighbor_col)))    # Pause for animation effect

    # Reconstruct and visualize the path from end to start
    current = app.end
    if current in parent or current == app.start:
        path=[]
        while current != app.start:
            path.append(current)
            current = parent.get(current)
             # Pause for animation effect
        path.append(app.start)
        app.draw_path_line(path)
    else:
        # No path found
        messagebox.showinfo("No Path", "No path found to the destination.")
