from queue import PriorityQueue
import pygame, math

class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size #x coordinate
        self.y = col * size #y coordinate
        self.color = (0, 0, 0)
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    def find_position(self):
        position = (self.row, self.col)
        return position
    
    def closed(self):
        return self.color == (255, 200, 240)
    
    def barrier(self):
        return self.color == (0,0,0)

    def open(self):
        return self.color == (255,255,255)
    
    def get_size(self):
        return self.size
    

#Heuristic function
def heuristic(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y) #Manhattan distance

#Create a grid with each box being a node
def create_grid(rows, size):
    grid = []
    node_size = size // rows  # Calculate the size of each node
    # Iterate over each row
    for i in range(rows):
        row = []  # Create a new row
        # Iterate over each column in the row
        for j in range(rows):
            node = Node(i, j, node_size, rows)  # Create a new node
            row.append(node)  # Add the node to the current row
        grid.append(row)  # Add the current row to the grid

    return grid