import logging
import argparse
import random
import time
import sys
import serial
from screen import Screen
import threading

class DigiPort(threading.Thread):
  def __init__(self, port):
    super().__init__(daemon=True)
    self.ser = serial.Serial(port, 9600, timeout=1)
    self.ram = [0] * 256

  def run(self):
    while True:
      self.ser.write(b's')
      self.ser.readline()
      registers = self.ser.readline()
      self.ser.write(b's')
      self.ser.readline()
      registers = self.ser.readline()
      self.ser.write(b'd')
      self.ser.readline()
      newram = []
      for i in range(16):
        data = self.ser.readline()
        data = data[6:54]
        data = [int(data[i:i+2],16) for i in range(0, len(data), 3)]
        newram += data
      if len(newram) == len(self.ram):
        self.ram = newram
      

class Digirule:
  def __init__(self, screen, controller, port):
    self.scr = screen
    self.ctrl = controller
    self.digi = DigiPort(port)
    self.pos = 0

  def up(self):
    self.pos = max(0, self.pos - 1)

  def down(self):
    self.pos = min(len(self.digi.ram) - self.scr.height , self.pos +1)

  def paint_data(self):
    for i in range(self.pos, self.pos + self.scr.height):
      y = i - self.pos
      for x in range(8):
        data = self.digi.ram[i] & (1 << x)
        self.scr.paint(x,y,data)

  def run(self):
    self.ctrl.start()
    self.digi.start()
    while True:
      cmd = self.ctrl.get()
      if cmd == 'exit':
        break
      elif cmd == 'left':
        self.up()
      elif cmd == 'right':
        self.down()
      self.scr.clear()
      self.paint_data()
      self.scr.update()
      
if __name__ == '__main__':
  parser = argparse.ArgumentParser("Digirule memory visualizer")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  parser.add_argument("-s", "--screen", action='store_true', help="Screen mode (disables the led matrix output)")
  parser.add_argument("-p", "--port", help="Serial port connected to digirule", default='/dev/ttyUSB0')
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
  t = Digirule(screen, controller, args.port)
  t.run()
