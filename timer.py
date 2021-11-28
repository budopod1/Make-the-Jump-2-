from time import time


class Timer:
  def __init__(self):
    self.time_len = 200
    self.start_time = 0
    self.granuality = 10
    self.running = False
  
  def add(self):
    self.time_len += self.granuality
  
  def remove(self):
    if self.time_len > self.granuality:
      self.time_len -= self.granuality
  
  def render(self):
    return self.time_len - (time() - self.start_time) if self.running else self.time_len

  def start(self):
    self.running = True
    self.reset()
  
  def reset(self):
    self.start_time = time()
  
  def stop(self):
    self.running = False
  
  def die(self):
    return self.render() < 0
