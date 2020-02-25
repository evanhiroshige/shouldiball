from datetime import datetime, timedelta
from DailyScheduleFetcher import DailyScheduleFetcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Booking import Booking
from CourtSchedule import CourtSchedule

DRIVER_PATH = '/Users/ehiroshige/dev/driver/chromedriver'


COURT_THREE_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=pw7uNs6e9v8qbfdIsvc5fDYq1MFunilYcWUxDMrP56yKqAjIwwaKA11U%2fQckiFjB2tWbX%2fc8606fDHS3t5PPuSnrcoE8cTQGmAOsO4wdf4ZaUfDtNt1OGQ%3d%3d'
COURT_TWO_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=8dCpAXZOtNUwCu7Xw7lFdvnMLXWJvC%2fXnljDAys%2fqmQx5OHc0kgRwku22rLLnqz9V187%2fQc5LcOubs4EolABUmZFwTbc8EyCREjolwr1Ekq69xl3QSidow%3d%3d'
SPORT_COURT_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=2sdeuuZ3cxh0hVZgJYA84txwBAjutRyjhYavKNQt%2f1ZU02OX1qeFfxh8QvnmqjnnvPoiPyTnIl8ZtHpxkgfPUK6dvglR7G8DdxFP69QIaS4hyDGPHot7LbGnj5jMFpqD'
COURT_SCHEDULE_URLS = [COURT_THREE_URL, COURT_TWO_URL, SPORT_COURT_URL]

court_name_to_url_map = {
  "Main Court": COURT_THREE_URL,
  "Middle Court": COURT_TWO_URL,
  "Sport Court": SPORT_COURT_URL
}

def get_basketball_courts_summary():
  sys.
  output = '\nMarino Court Schedule:\n'
  court_schedules = fetch_court_schedules_for_today()
  now = datetime.now()
  open_court_count = 0
  for court_schedule in court_schedules:
    no_booking_on_court = True
    for booking in court_schedule.bookings:
      if booking.isScheduledDuring(now):
        d = datetime.strptime(str(booking.end_time.time()), "%H:%M:%S")
        output += court_schedule.name + ": " + booking.name + " until " +  d.strftime("%I:%M %p") + '\n'
        no_booking_on_court = False
        if booking.name == 'Open Basketball':
          open_court_count += 1
    if no_booking_on_court:
      next_booking = court_schedule.getNextBooking(now)
      next_booking_start_time_template = '01:00:00' if next_booking == None else str(next_booking.start_time)
      d = datetime.strptime(next_booking_start_time_template, "%H:%M:%S")
      output += court_schedule.name + ": Open Basketball until " + d.strftime("%I:%M %p") + '\n'
      open_court_count += 1
    courtWord = 'court' if open_court_count == 1 else 'courts'
  output += '\n' + str(open_court_count) + ' ' + courtWord + ' currently open.\n'
  return output


def fetch_court_schedules_for_today():
  driver = webdriver.Chrome(DRIVER_PATH)
  driver.implicitly_wait(10)
  schedules = []
  today = datetime.today()
  day_of_month = str((today.day))
  try:
    for court_name in court_name_to_url_map.keys():
      schedule_fetcher = DailyScheduleFetcher(driver)
      court_bookings = schedule_fetcher.fetch(court_name_to_url_map[court_name], day_of_month)
      schedules.append(CourtSchedule(court_name, court_bookings))
  finally:
    driver.quit()
  return schedules



