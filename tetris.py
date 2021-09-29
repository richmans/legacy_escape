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
  
class Stack:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.reset()
  
  def reset(self):
    self.data = [[False] * self.width for _ in range(self.height)]
  
  def collapse(self):
    # Remove all rows that are full
    self.data = [r for r in self.data if not all(r)]
    # Append empty rows at the top
    while len(self.data) < self.height:
      self.data.insert(0, [False] * self.width)
      
  def land(self, tetromino, x, y):
    for tx in range(tetromino.width):
      for ty in range(tetromino.height):
        self.data[y + ty][x + tx] |= tetromino.data[ty][tx]

  def collision(self, tetromino, x, y):
    for tx in range(tetromino.width):
      for ty in range(tetromino.height):
        if self.data[y + ty][x + tx] and tetromino.data[ty][tx]:
          return True
    return False

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
    self.scr = screen
    self.ctrl = controller
    self.stack = Stack(screen.width, screen.height)
    self.reset()
  
  def lost(self):
    self.reset()
    
  
  def reset(self):
    self.stack.reset()
    self.select_tetromino()

  def select_tetromino(self):
    self.current = deepcopy(random.choice(self.tetrominos))
    self.y = 0
    self.x = math.ceil((8 - self.current.width) / 2)
    if self.stack.collision(self.current, self.x, self.y):
      self.lost()

  def paint_data(self, data, atx, aty):
    y = aty
    for r in data:
      x = atx
      for c in r:
        if c:
          self.scr.on(x,y)
        x += 1
      y += 1

  def is_landed(self):
    if self.current.height + self.y >= self.scr.height:
      return True
    if self.stack.collision(self.current, self.x, self.y + 1):
      return True
    return False

  def update_position(self):
    if self.is_landed():
      self.stack.land(self.current, self.x, self.y)
      self.stack.collapse()
      self.select_tetromino()
    else:
      self.y += 1
    
  def rotate(self):
    if self.x + self.current.height >= self.scr.width:
      return
    rotated = self.current.rotated()
    if not self.stack.collision(rotated, self.x, self.y):
      self.current = rotated
  
  def left(self):
    if self.x <= 0:
      return
    if not self.stack.collision(self.current, self.x -1 , self.y):
      self.x -= 1

  def right(self):
    if self.x + self.current.width >= self.scr.width:
      return
    if not self.stack.collision(self.current, self.x +1 , self.y):
      self.x += 1

  def run(self):
    self.ctrl.start()
    while True:
      cmd = self.ctrl.get()
      if cmd == 'exit':
        break
      elif cmd == 'rotate':
        self.rotate()
      elif cmd == 'left':
        self.left()
      elif cmd == 'right':
        self.right()
      self.update_position()
      self.scr.clear()
      self.paint_data(self.stack.data, 0, 0)
      self.paint_data(self.current.data, self.x, self.y)
      self.scr.update()
      time.sleep(0.2)


if __name__ == '__main__':
  parser = argparse.ArgumentParser("Tetris game on the led matrix")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  parser.add_argument("-s", "--screen", action='store_true', help="Screen mode (disables the led matrix output)")
  parser.add_argument("-k", "--keyboard", action='store_true', help="Keyboard mode (disables the rotary controller)")
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
  if args.keyboard:
    from keyboard_controller import KeyboardController
    controller = KeyboardController()
  else:
    try:
      from rotary_controller import RotaryController
    except ModuleNotFoundError:
      print("Could not load rotary controller module. either `pip3 install evdev` or use the --keyboard flag", file=sys.stderr)
      sys.exit(1)
    controller = RotaryController()
  screen = Screen(8,32, matrix)
  t = Tetris(screen, controller)
  t.run()
