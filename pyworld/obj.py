class Obj:
  def __init__(self):
    self.active = True
    self.event_handlers = []

  def event(self, event):
    if self.active:
      for event_handler in self.event_handlers:
        if event_handler[0] == event.type:
          event_handler[1](event)

  def on(self, event_type, event_handler):
    self.event_handlers.append([event_type, event_handler])


