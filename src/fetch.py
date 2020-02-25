
import datetime
from DailyScheduleFetcher import DailyScheduleFetcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Booking import Booking

COURT_THREE_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=pw7uNs6e9v8qbfdIsvc5fDYq1MFunilYcWUxDMrP56yKqAjIwwaKA11U%2fQckiFjB2tWbX%2fc8606fDHS3t5PPuSnrcoE8cTQGmAOsO4wdf4ZaUfDtNt1OGQ%3d%3d'
COURT_TWO_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=8dCpAXZOtNUwCu7Xw7lFdvnMLXWJvC%2fXnljDAys%2fqmQx5OHc0kgRwku22rLLnqz9V187%2fQc5LcOubs4EolABUmZFwTbc8EyCREjolwr1Ekq69xl3QSidow%3d%3d'
SPORT_COURT_URL = 'https://nuevents.neu.edu/CustomBrowseEvents.aspx?data=2sdeuuZ3cxh0hVZgJYA84txwBAjutRyjhYavKNQt%2f1ZU02OX1qeFfxh8QvnmqjnnvPoiPyTnIl8ZtHpxkgfPUK6dvglR7G8DdxFP69QIaS4hyDGPHot7LbGnj5jMFpqD'
COURT_SCHEDULE_URLS = [COURT_THREE_URL]#, COURT_TWO_URL, SPORT_COURT_URL]

DRIVER_PATH = '/Users/ehiroshige/dev/driver/chromedriver'

def get_courts_summary():
  schedules = fetch_courts_schedule()
  print(datetime.datetime.now())
  for schedule in schedules:
    for booking in schedule:
      print(booking.name, booking.start_time, booking.end_time)

      if booking.isScheduledDuring(datetime.datetime.now()):
        print(booking.name, booking.start_time, booking.end_time)


def fetch_courts_schedule():
  driver = webdriver.Chrome(DRIVER_PATH)
  driver.implicitly_wait(10)
  schedules = []
  today = datetime.datetime.today()
  day_of_month = str((today.day - 1))
  try:
    for url in COURT_SCHEDULE_URLS:
      schedule_fetcher = DailyScheduleFetcher(driver)
      court_schedule = schedule_fetcher.fetch(url, "24")
      schedules.append(court_schedule)
  finally:
    driver.quit()
  return schedules

if __name__ == "__main__":
  get_courts_summary()



