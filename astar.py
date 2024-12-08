import time  # For animation delays
from tkinter import messagebox
from heapq import heappush, heappop

# Constants (ensure these match those in main.py)
GRID_SIZE = 20
CELL_SIZE = 20

START_COLOR = "green"
END_COLOR = "red"
PATH_COLOR = "yellow"
VISITED_COLOR = "purple"
OBSTACLE_COLOR = "black"
EMPTY_COLOR = "white"

# Directions for movement (Right, Down, Left, Up)
DIRECTIONS = [
    (0, 1),   # Right
    (1, 0),   # Down
    (0, -1),  # Left
    (-1, 0)   # Up
]

def heuristic(a, b):
    """Calculate the Manhattan distance between two points a and b."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_astar(app):
    """Run the A* algorithm to find the shortest path from start to end."""
    # Clear previous paths and visited cells
    clear_search(app)

    start = app.start
    end = app.end

    open_set = []
    heappush(open_set, (0, start))

    came_from = {}  # For path reconstruction
    
    # Fixed dictionary comprehension for g_score and f_score
    g_score = {}
    f_score = {}
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            g_score[(row, col)] = float('inf')
            f_score[(row, col)] = float('inf')
    
    g_score[start] = 0
    f_score[start] = heuristic(start, end)

    open_set_hash = {start}

    while open_set:
        current = heappop(open_set)[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(app, came_from, current)
            return

        for direction in DIRECTIONS:
            neighbor_row = current[0] + direction[0]
            neighbor_col = current[1] + direction[1]
            neighbor = (neighbor_row, neighbor_col)

            # Check if neighbor is within the grid bounds
            if 0 <= neighbor_row < GRID_SIZE and 0 <= neighbor_col < GRID_SIZE:
                # Check if neighbor is not an obstacle
                if app.grid[neighbor_row][neighbor_col]["distance"] != -1:
                    tentative_g_score = g_score[current] + 1

                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                        if neighbor not in open_set_hash:
                            heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)
                            # Visualize the neighbor
                            if neighbor != end:
                                app.canvas.itemconfig(
                                    app.grid[neighbor_row][neighbor_col]["canva"],
                                    fill=VISITED_COLOR
                                )
                    app.root.update()
                    time.sleep(0.01)

    # If we reach here, no path was found
    messagebox.showinfo("No Path", "No path found to the destination.")

def reconstruct_path(app, came_from, current):
    """Reconstruct the path from start to end."""
    while current in came_from:
        if current != app.start and current != app.end:
            app.canvas.itemconfig(
                app.grid[current[0]][current[1]]["canva"],
                fill=PATH_COLOR
            )
        current = came_from[current]
        app.root.update()
        time.sleep(0.02)

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
    app.root.update()