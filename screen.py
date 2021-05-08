
class Screen:
  def __init__(self, width,height, output):
    self.width = width
    self.height = height
    self.output = output
    self.clear()
  
  def on(self, x, y):
    self.data[y][x] = True
  
  def off(self, x , y):
    self.data[y][x] = False

  def paint(self, x, y, v):
    self.data[y][x] = v

  def clear(self):
    self.data = [[False] * self.width for _ in range(self.height)]

  def update(self):
    self.output.update(self)

  def __repr__(self):
    return "\r\n".join(["".join(['O' if c else ' ' for c in r]) for r in self.data])

  