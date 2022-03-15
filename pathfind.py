def edges(cols, rows):
  e = []
  for i in range(rows - 1):
    # top
    e.append((0, i))
    # bottom
    e.append((cols - 1, i))

  for i in range(cols - 1):
    # left
    e.append((i, 0))
    # right
    e.append((i, rows - 1))

  # lower right corner
  e.append((cols - 1, rows - 1))

  return e


class Route:
  def __init__(self, cells):
    self.cells = cells
    
    if len(cells) > 0:
      self.path = [cell.position for cell in cells]
      self.score = sum([cell.f_score for cell in cells]) / len(cells)
    else:
      self.path = []
      self.score = 100 # some random high value?

  def get_current(self):
    return self.path[0]

  def pop_next(self):
    if len(self.path) > 1:
      self.path.pop(0)
    return self.path[0]


class Cell:
  def __init__(self, parent, position):
    self.parent = parent
    self.position = position

    self.g_score = 0
    self.h_score = 0
    self.f_score = 0

  def __eq__(self, other):
    return self.position == other.position


def find_nearest_route(grid, current, cols, rows):
  fastest_route = []
  for pos in edges(cols, rows):
    route = Route(find_route(grid, current, pos))
    
    if not fastest_route or route.score < fastest_route.score:
      fastest_route = route

  return fastest_route
    

def find_route(grid, start, end):
  start_cell = Cell(None, start)
  end_cell = Cell(None, end)

  open_set = []
  closed_set = []

  open_set.append(start_cell)

  N_CELLS = 0
  MAX_CELLS = len(grid) * len(grid[0])

  if grid[end[0]][end[1]] != 0:
    return []

  while len(open_set) > 0:
    N_CELLS += 1
    # if we have searched too many cells (impossible path? maybe this also catches possible paths, but i doubt it)
    if N_CELLS >= MAX_CELLS:
      return []
    
    current_cell = open_set[0]
    current_index = 0
    for index, cell in enumerate(open_set):
      if cell.f_score < current_cell.f_score:
        current_cell = cell
        current_index = index

    open_set.pop(current_index)
    closed_set.append(current_cell)

    if current_cell == end_cell:
      path = []
      current = current_cell
      while current is not None:
        path.append(current)
        current = current.parent
        
      return path[::-1]

    neighbors = []
    for neighbor in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
      cell_position = (current_cell.position[0] + neighbor[0], current_cell.position[1] + neighbor[1])

      if cell_position[0] > (len(grid) - 1) or cell_position[0] < 0 or cell_position[1] > (len(grid[len(grid)-1]) -1) or cell_position[1] < 0:
        continue

      if grid[cell_position[0]][cell_position[1]] != 0:
        continue

      new_cell = Cell(current_cell, cell_position)
      neighbors.append(new_cell)

    for neighbor in neighbors:
      for closed_neighbor in closed_set:
        if neighbor == closed_neighbor:
          continue
      
      neighbor.g_score = current_cell.g_score + 1
      neighbor.h_score = ((neighbor.position[0] - end_cell.position[0]) ** 2) + ((neighbor.position[1] - end_cell.position[1]) ** 2)
      neighbor.f_score = neighbor.g_score + neighbor.h_score

      for open_cell in open_set:
        if neighbor == open_cell and neighbor.g_score > open_cell.g_score:
          continue

      open_set.append(neighbor)
