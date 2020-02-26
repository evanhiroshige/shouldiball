class CourtSchedule:
  def __init__(self, name, bookings):
    self.name = name
    self.bookings = bookings

  # Returns next booking which start after time, null if no booking
  def getNextBooking(self, time):
    min_start_time = None
    for booking in self.bookings:
      booking_time = booking.start_time
      if booking_time > time and (min_start_time == None or booking_time < min_start_time):
        min_start_time = booking_time
    return min_start_time
