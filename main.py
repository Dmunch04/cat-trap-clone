import pygame
from grid import Grid
from pathfind import find_nearest_route, edges


class Game:
  def __init__(self, rows=12, columns=12, start=(6, 6)):
    self.rows = rows
    self.cols = columns
    
    self.grid = Grid(rows, columns, start)
    
    self.player_turn = True

    self.screen = pygame.display.set_mode((800, 600))
    self.clock = pygame.time.Clock()
    self.run = True
    self.tick = 60

    self.last_route = None

  def loop(self):
    while self.run:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.run = False

        if self.player_turn:
          if event.type == pygame.MOUSEBUTTONDOWN:
            if self.grid.node_pressed(event.pos):
              self.player_turn = False

      if not self.player_turn:
        route = find_nearest_route(self.grid.get_raw(), self.grid.player_pos, self.cols, self.rows)

        if route == [] or route.path == []:
          self.run = False
          print('Player won!')
        else:
          next_pos = route.path[1]

          if next_pos in edges(self.cols, self.rows):
            self.run = False
            print('AI won!')
          else:
            self.grid.move_player(next_pos[0], next_pos[1])
          
          self.player_turn = True

      self.screen.fill((0, 0, 0))
      self.grid.draw_grid(self.screen)

      pygame.display.update()
      self.clock.tick(self.tick)

  pygame.quit()

if __name__ == '__main__':
  game = Game()
  game.loop()
