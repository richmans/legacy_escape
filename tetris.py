import logging
import argparse
from led_matrix import LEDMatrix
import random
from copy import deepcopy
import math
import time

class Tetromino:
  def __init__(self, name, data):
    self.data = data
    self.name = name
    self.width = len(self.data[0])
    self.height = len(self.data)

class Tetris:
  tetrominos = [
    Tetromino("O", [[True,True], [True,True]]),
    Tetromino("I", [[True],[True],[True],[True]]),
    Tetromino("S", [[False, True, True], [True, True, False]]),
    Tetromino("Z", [[True, True, False], [False, True,True]]),
    Tetromino("L", [[True, False], [True, False], [True, True]]),
    Tetromino("J", [[False, True], [False, True], [True, True]]),
    Tetromino("T", [[True, True, True], [False, True, False]])
  ]

  def __init__(self):
    self.m = LEDMatrix()
    self.s = self.m.screen
    self.select_tetromino()
    
  def select_tetromino(self):
    self.current = deepcopy(random.choice(self.tetrominos))
    self.y = 0
    self.x = math.ceil((8 - self.current.width) / 2)

  def paint_tetromino(self):
    y = self.y
    for r in self.current.data:
      x = self.x
      for c in r:
        self.s.paint(x,y,c)
        x += 1
      y += 1

  def is_landed(self):
    return self.current.height + self.y >= 32

  def update_position(self):
    if self.is_landed():
      self.select_tetromino()
    else:
      self.y += 1
    
  def run(self):
    while True:
      self.update_position()
      self.s.clear()
      self.paint_tetromino()
      self.m.update()
      time.sleep(0.2)


if __name__ == '__main__':
  parser = argparse.ArgumentParser("Tetris game on the led matrix")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  t = Tetris()
  t.run()
