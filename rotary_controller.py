import threading
import evdev
import select
class RotaryController(threading.Thread):
  def __init__(self):
    super().__init__(daemon=True)
    self.cmd = None
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    self.devices = {dev.fd: dev for dev in devices}

  def get(self):
    # There is a race condition here. I don't care.
    cmd = self.cmd
    if cmd is not None:
      self.cmd = None
    return cmd

  def get_event(self):
    r, w, x = select.select(self.devices, [], [])
    if len(r) > 0:
      fd = r[0]
      events = list(self.devices[fd].read())
      if len(events) > 0:
        event = evdev.util.categorize(events[0])
        return event
    return None

  def set_command(self, event):
    if isinstance(event, evdev.events.RelEvent):
      value = event.event.value
      if value == 1:
        self.cmd = 'right'
      elif value == -1:
        self.cmd = 'left'
    elif isinstance(event, evdev.events.KeyEvent):
      if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
        self.cmd = 'rotate'

  def run(self):
    while True:
      evt = self.get_event()
      self.set_command(evt)
