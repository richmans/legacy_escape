class ScreenMatrix:
  def update(self, screen):
    print(chr(27) + "[2J")
    print(screen, end=None)