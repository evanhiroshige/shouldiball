from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Booking import Booking
from datetime import datetime, timedelta
import pytz

NY_TIMEZONE = pytz.timezone('America/New_York')

class DailyScheduleFetcher:

  def __init__(self, driver):
    self.driver = driver

  def fetch(self, URL, day):
    self.driver.get(URL)
    daily_elements = self.get_daily_elements()
    daily_schedule = self.get_daily_schedule(daily_elements, day)
    return daily_schedule

  def get_daily_elements(self):
    weekly_schedule_element = self.driver.find_element_by_id('weeklyResults')
    return weekly_schedule_element.find_elements_by_class_name('calendar-cell-container')

  def get_daily_schedule(self, daily_elements, day_of_month):
    for day_element in daily_elements:
      date_element = day_element.find_element_by_class_name('calendar-event')

      if (date_element.text == day_of_month):
        events = day_element.find_elements_by_class_name('booking-event')
        return self.parse_events_to_daily_schedule(events)

  def parse_events_to_daily_schedule(self, events):
    bookings = []
    for event in events:
      event_name = event.find_element_by_xpath('.//div[1]/span').text
      event_time_start = event.find_element_by_xpath('.//div[2]/span[1]').text
      event_time_end = event.find_element_by_xpath('.//div[2]/span[2]').text
      bookings.append(self.build_booking(event_name, event_time_start, event_time_end))
      print(event_name + " from " + event_time_start + " " + event_time_end)
    return bookings

  def build_booking(self, event_name, event_time_start, event_time_end):
    time = self.get_formatted_time(event_time_start, event_time_end)
    return Booking(event_name, time[0], time[1])

  def get_formatted_time(self, event_time_start, event_time_end):
    datetime_NY = datetime.now(NY_TIMEZONE)
    start_date = datetime_NY.today()
    end_date = datetime_NY.today()
    start_time = datetime_NY.strptime(event_time_start, '%I:%M%p')
    start_date_time = datetime_NY.combine(start_date, start_time.time())

    end_time = datetime_NY.strptime(event_time_end, '- %I:%M%p')
    end_date_time = datetime_NY.combine(end_date, end_time.time())
    if start_date_time.hour >= 12:
      tomorrow = datetime.now() + timedelta(days=1)
      end_date_time = datetime_NY.combine(tomorrow.date(), end_time.time())

    return (start_date_time, end_date_time)


