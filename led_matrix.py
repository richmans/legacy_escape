import spidev
import time
import argparse
import logging
from copy import deepcopy
from screen import Screen

class LEDMatrix:
  def __init__(self, bus=0, device=0, rotate=1):
    self.bus = bus
    self.device = device
    self.rotate = rotate
    self.spi = spidev.SpiDev()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 8000000
    self.send([0xb, 7]*4)
    self.send([0x9, 0]*4)
    self.send([0xc, 1]*4)
    self.send([0xa, 0x1]*4)
    self.send([0xf, 0]*4)

  def send(self, cmd):
    logging.debug(">> %s", cmd)
    self.spi.xfer(list(cmd))
  
  def row_to_int(self, r):
    res = 0
    for i in r:
      res = res << 1
      if i:
        res +=1
    return res

  def update(self, screen):
    data = screen.data
    parts = [data[i:i + 8] for i in range(0, len(data), 8)]
    parts.reverse()
    parts = [list(zip(*p[::-1])) for p in parts]
    for i in range(8):
      data = []
      for p in parts:
        data.append(i+1)
        data.append(self.row_to_int(p[i]))
      self.send(data)

  def test(self, screen):
    logging.info("Testing...")
    ypos = 0
    xpos = 0
    spd = 1
    while True:
      screen.clear()
      screen.on(xpos , ypos)
      ypos = (ypos + 1) % 32
      xpos = xpos + spd
      if xpos == 7 or xpos == 0:
        spd = -1 * spd
      screen.update()
      time.sleep(0.04)

if __name__ == '__main__':
  parser = argparse.ArgumentParser("LED Matrix test program")
  parser.add_argument("-d", "--debug", action='store_true', help="Enable debug output")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)
  m = LEDMatrix()
  s = Screen(8,32,m)
  m.test(s)
