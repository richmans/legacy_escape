class ScreenMatrix:
  def update(self, screen):
    print(chr(27) + "[2J\r", end=None)
    print(screen, end=None)