import threading
class RotaryController(threading.Thread):
  def __init__(self):
    super().__init__(daemon=True)
    self.cmd = None

  def get(self):
    # There is a race condition here. I don't care.
    cmd = self.cmd
    if cmd is not None:
      self.cmd = None
    return cmd

  def get_event(self):
    return None
    
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
      ch = self.get_event()
      self.set_command(ch)
      if self.cmd == 'exit':
        break