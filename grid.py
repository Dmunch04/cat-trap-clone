import random
import pygame
from pathfind import edges


class NodeState:
  EMPTY = 0
  WALL = 1
  PLAYER = 2

  @staticmethod
  def get_color(state):
    if state == 0:
      return 'WHITE'
    elif state == 1:
      return 'RED'
    elif state == '2':
      return 'GREEN'
    else:
      return 'BLUE'
      

class GridNode:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.state = NodeState.EMPTY

    self.rect = pygame.Rect((self.x * 10 + (self.x * 5)), (self.y * 10 + (self.y * 5)), 10, 10)

  def update_state(self, new_state):
    self.state = new_state

  def draw(self, screen):
    pygame.draw.rect(screen, NodeState.get_color(self.state), self.rect)


class Grid:
  def __init__(self, rows, columns, start, obstacle_range=(10, 20)):
    self.rows = rows
    self.cols = columns
    self.start = start
    self.obstacle_range = obstacle_range

    self.grid = [[GridNode(j, i) for i in range(rows)] for j in range(columns)]
    self.grid[start[0]][start[1]].update_state(NodeState.PLAYER)
    self.place_obstacles()

    self.player_pos = start

  def place_obstacles(self):
    n = random.randint(self.obstacle_range[0], self.obstacle_range[1])

    for i in range(n):
      placed = False
      while not placed:
        x = random.randint(0, self.cols - 1)
        y = random.randint(0, self.rows - 1)
  
        if self.node_empty(x, y):
          self.place_wall(x, y)
          placed = True

  def move_index_to_pos(self, index):
    from math import floor

    row = max(0, min(floor(int(f"{(index - 1):02}") / self.rows), self.rows - 1))
    col = max(0, min(int(index / (row + 1)), self.cols)) - 1

    return (col, row)

  def pos_to_move_index(self, x, y):
    #row = self.rows * x
    #return row + y
    pass #?

  def get_node(self, x, y):
    return self.grid[x][y]

  def node_empty(self, x, y):
    return self.get_node(x, y).state == NodeState.EMPTY

  def move_player(self, x, y):
    if self.node_empty(x, y):
      self.grid[self.player_pos[0]][self.player_pos[1]].update_state(NodeState.EMPTY)
      self.grid[x][y].update_state(NodeState.PLAYER)
      self.player_pos = (x, y)
      return True

    return False

  def place_wall(self, x, y):
    if self.node_empty(x, y):
      self.grid[x][y].update_state(NodeState.WALL)
      return True

    return False

  def node_pressed(self, mouse_pos):
    for row in self.grid:
      for node in row:
        if node.rect.collidepoint(mouse_pos):
          return self.place_wall(node.x, node.y)

    return False

  def draw_grid(self, screen):
    for row in self.grid:
      for node in row:
        node.draw(screen)

  def get_raw(self):
    return [[node.state for node in self.grid[i]] for i in range(len(self.grid))]
