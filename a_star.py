import pygame
import math
import time
from queue import PriorityQueue
from copy import deepcopy

# Initialize pygame
pygame.init()

# Maze constants
ORIG_GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
]
GRID = deepcopy(ORIG_GRID)
ROWS = len(GRID)
START = (0,0)
END = (9,9)

# Initialize window
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Demonstration")

# Color Constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (80, 80, 80)
DARK_GREY = (30, 30, 30)
COLORS = [
    WHITE,      # Empty
    DARK_GREY,  # Wall
    GREEN,      # Open   
    RED,        # Closed
    BLUE,       # Found
    YELLOW      # Start/End
]


# Color grid position at p
def color_grid(p, color):
    GRID[p[0]][p[1]] = color

# Heuristic function
def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Return valid neighbors of point in grid
def get_neighbors(p):
    MOVES = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []
    for m in MOVES:
        new_x = p[0] + m[0]
        new_y = p[1] + m[1]
        if (0 <= new_x <= len(GRID)-1 and
        0 <= new_y <= len(GRID)-1
        and GRID[new_x][new_y] != 1):
            neighbors.append( (new_x, new_y) )
    return neighbors
    
# A*
def a_star():
    frontier = PriorityQueue()
    frontier.put((0, START))  # Store as (priority, node)
    came_from = {}
    came_from[START] = None
    cost_map = {}
    cost_map[START] = 0
    color_grid(START, 5)

    while not frontier.empty():
        current_priority, current = frontier.get()
        color_grid(current, 3)
        
        if current == END:
            break
        
        cur_neighbors = get_neighbors(current)
        for neighbor in cur_neighbors:
            new_cost = cost_map[current] + 2  
            if neighbor not in cost_map or new_cost < cost_map[neighbor]:
                cost_map[neighbor] = new_cost
                priority = new_cost + h(neighbor, END)
                frontier.put((priority, neighbor))
                came_from[neighbor] = current
                color_grid(neighbor, 2)
        draw()
        time.sleep(0.04)

    # Reconstruct path
    cur = END
    while cur is not None:
        color_grid(cur, 5)
        temp = came_from[cur]
        cur = temp
        draw()
        time.sleep(0.02)

# Draw grid
def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(WIN, COLORS[GRID[i][j]], (j * gap,  i * gap, gap, gap))
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * gap), (WIDTH, i * gap))
    for j in range(ROWS):
        pygame.draw.line(WIN, GREY, (j * gap, 0), (j * gap, WIDTH))

# Draw window
def draw():
    WIN.fill(WHITE)
    draw_grid()
    pygame.display.update()
    
# Main control loop
def main():
    running = True
    while running:
        draw()
        for event in pygame.event.get():
            # Exit Program
            if event.type == pygame.QUIT:
                running = False
            # Keyboard input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Exit Program
                    running = False
                if event.key == pygame.K_SPACE: # Start A*
                    a_star()
                if event.key == pygame.K_a:
                    global GRID
                    GRID = deepcopy(ORIG_GRID)  # Reset GRID using deepcopy
                
    pygame.quit()
    
main()