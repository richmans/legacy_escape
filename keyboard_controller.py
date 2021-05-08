import termios, sys , tty
import threading
class KeyboardController(threading.Thread):
  def __init__(self):
    super().__init__(daemon=True)
    self.cmd = None

  def getch(self):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1) 
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

  def get(self):
    # There is a race condition here. I don't care.
    cmd = self.cmd
    if cmd is not None:
      self.cmd = None
    return cmd

  def set_command(self, ch):
    if ch == 'q':
      self.cmd = 'exit'
    elif ch == 'a':
      self.cmd = 'left'
    elif ch == 'f':
      self.cmd = 'right'
    elif ch == 'd':
      self.cmd = 'drop'
    elif ch == 's':
      self.cmd = 'rotate'

  def run(self):
    while True:
      ch = self.getch()
      self.set_command(ch)
      if self.cmd == 'exit':
        break