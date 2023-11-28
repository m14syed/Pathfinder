import pygame

class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size #x coordinate
        self.y = col * size #y coordinate
        self.color = (255, 255, 255)
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    def __lt__(self, other):
        return False

    def find_position(self):
        position = (self.row, self.col)
        return position
    
    def start(self):
        return self.color == (0, 255, 0) #Green
    
    def make_start(self):
        self.color = (0, 255, 0) 

    def end(self):
        return self.color == (255, 0, 0) #Red

    def make_end(self):
        self.color = (255, 0, 0) 
    
    def open(self):
        return self.color == (0, 0, 255) #Blue
    
    def make_open(self):
        self.color = (0, 0, 255) 

    def closed(self):
        return self.color == (127, 127, 127) #Gray
    
    def make_closed(self):
        self.color = (127, 127, 127) 
    
    def barrier(self):
        return self.color == (0, 0, 0) #Black
    
    def make_barrier(self):
        self.color = (0, 0, 0)
        
    def start_over(self):
        self.color = (255, 255, 255) #White
    
    def make_path(self):
        self.color = (255, 255, 0) #Yellow
    
    def get_size(self):
        return self.size
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size)) #Draw the node

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

        for dx, dy in directions: #Check each direction
            new_row, new_col = self.row + dx, self.col + dy #New row and column
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows: #Check if the new row and column are in the grid
                if not grid[new_row][new_col].barrier(): #Check if the new node is a barrier
                    self.neighbors.append(grid[new_row][new_col]) #Add the new node to the neighbors list

#Make the window and Title
WIN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Pathfinding Visualizer")

#Heuristic function
def heuristic(node1, node2):
	x1, y1 = node1
	x2, y2 = node2
	return abs(x1 - x2) + abs(y1 - y2)

#Create a grid with each box being a node
def create_grid(rows, size):
    grid = []
    node_size = size // rows  # Calculate the size of each node

    for i in range(rows):
        row = []  # Create a new row
        for j in range(rows):
            node = Node(i, j, node_size, rows)  # Create a new node
            row.append(node)  # Add the node to the current row

        grid.append(row)  # Add the current row to the grid

    return grid

#Draw the grid
def draw(win, grid, rows, size):
    node_size = size // rows  # Calculate the size of each node
    win.fill((0, 0, 0))  # Fill the window with black

    for row in grid:
        for node in row:
            node.draw(win)  # Draw each node

    for i in range(rows):
        pygame.draw.line(win, (0, 0, 0), (0, i * node_size), (size, i * node_size))  # Draw a horizontal line
        for j in range(rows):
            pygame.draw.line(win, (0, 0, 0), (j * node_size, 0), (j * node_size, size))  # Draw a vertical line  # Draw the grid

    pygame.display.update()  # Update the display

#Get the position (row and column) of the mouse
def mouse_position(pos, rows, size):
    node_size = size // rows  # Calculate the size of each node
    x, y = pos

    row = x // node_size
    col = y // node_size

    return row, col

#Reconstruct the path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

#A* Search Algorithm
def a_star_algorithm(draw, grid, start, end):
    open_set = [start] #Nodes to be evaluated
    came_from = {}  # Keep track of the path
    g_score = {node: float("inf") for row in grid for node in row} # Keep track of the g score
    g_score[start] = 0 
    f_score = {node: float("inf") for row in grid for node in row} # Keep track of the f score
    f_score[start] = heuristic(start.find_position(), end.find_position()) #Calculate the f score


    while open_set: #While there are nodes to be evaluated
        open_set.sort(key=lambda node: f_score[node])
        current = open_set.pop(0)

        if current == end: #If the current node is the end node
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors: #Check each neighbor
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]: #If the g score is less than the neighbor's g score
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.find_position(), end.find_position())
                if neighbor not in open_set:
                    open_set.append(neighbor)
                    neighbor.make_open()

        draw()

    return False 


def main(win, size):
    numRows = 50
    grid = create_grid(numRows, size)

    run = True
    start = None
    end = None

    while run:
        draw(win, grid, numRows, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Create the start, end, and barriers
            if pygame.mouse.get_pressed()[0]: 
                pos = pygame.mouse.get_pos()
                row, col = mouse_position(pos, numRows, size)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            #Remove the node
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_position(pos, numRows, size)
                node = grid[row][col]
                node.start_over()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            #Start the algorithm
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_s and start and end: 
                    for row in grid: 
                        for node in row: 
                            node.update_neighbors(grid) 
                    a_star_algorithm(lambda: draw(win, grid, numRows, size), grid, start, end) 

                #reset the grid
                if event.key == pygame.K_c: 
                    start = None 
                    end = None
                    grid = create_grid(numRows, size)
            
    pygame.quit()

main(WIN, 800)