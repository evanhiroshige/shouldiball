class Booking:
  def __init__(self, name, start_time, end_time):
    self.name = name
    self.start_time = start_time
    self.end_time = end_time

  def isScheduledDuring(self, time):
    return self.start_time <= time <= self.end_time