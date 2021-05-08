import logging
import argparse
import random
from copy import deepcopy
import math
import time
import sys
from screen import Screen
class Tetromino:
  def __init__(self, name, data):
    self.data = data
    self.name = name
    self.measure()

  def measure(self):
    self.width = len(self.data[0])
    self.height = len(self.data)

  def rotated(self):
    rotated_data = list(zip(*self.data[::-1]))
    return Tetromino(self.name, rotated_data)
    
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

  def __init__(self, screen, controller):
    self.s = screen
    self.c = controller
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
    
  def rotate(self):
    if self.x + self.current.height >= self.s.width:
      return
    self.current = self.current.rotated()
  
  def left(self):
    if self.x > 0:
      self.x -= 1
  
  def right(self):
    if self.x + self.current.width < self.s.width:
      self.x += 1
  def run(self):
    self.c.start()
    while True:
      cmd = self.c.get()
      if cmd == 'exit':
        break
      elif cmd == 'rotate':
        self.rotate()
      elif cmd == 'left':
        self.left()
      elif cmd == 'right':
        self.right()
      self.update_position()
      self.s.clear()
      self.paint_tetromino()
      self.s.update()
      time.sleep(0.2)


if __name__ == '__main__':
  parser = argparse.ArgumentParser("Tetris game on the led matrix")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  parser.add_argument("-s", "--screen", action='store_true', help="Screen mode (disables the led matrix output)")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  if args.screen:
    from screen_matrix import ScreenMatrix
    matrix = ScreenMatrix()
  else:
    try:
      from led_matrix import LEDMatrix
    except ModuleNotFoundError:
      print("Could not load matrix module. either `pip3 install spidev` or use the --screen flag", file=sys.stderr)
      sys.exit(1)
    matrix = LEDMatrix()
  from keyboard_controller import KeyboardController
  controller = KeyboardController()
  screen = Screen(8,32, matrix)
  t = Tetris(screen, controller)
  t.run()
