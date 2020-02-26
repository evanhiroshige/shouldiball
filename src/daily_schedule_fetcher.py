from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking import Booking
from datetime import datetime, timedelta

class DailyScheduleFetcher:

  def __init__(self, driver, now):
    self.now = now
    self.driver = driver

  def fetch(self, URL, day):
    self.driver.get(URL)
    daily_elements = self._get_daily_elements()
    daily_schedule = self._get_daily_schedule(daily_elements, day)
    return daily_schedule

  def _get_daily_elements(self):
    weekly_schedule_element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'weeklyResults')))
    return weekly_schedule_element.find_elements_by_class_name('calendar-cell-container')

  def _get_daily_schedule(self, daily_elements, day_of_month):
    for day_element in daily_elements:
      date_element = day_element.find_element_by_class_name('calendar-event')
      if (date_element.text == day_of_month):
        events = day_element.find_elements_by_class_name('booking-event')
        return self._parse_events_to_daily_bookings(events)

  def _parse_events_to_daily_bookings(self, events):
    bookings = []
    for event in events:
      event_name = event.find_element_by_xpath('.//div[1]/span').text
      event_time_start = event.find_element_by_xpath('.//div[2]/span[1]').text
      event_time_end = event.find_element_by_xpath('.//div[2]/span[2]').text
      bookings.append(self._build_booking(event_name, event_time_start, event_time_end))
    return bookings

  def _build_booking(self, event_name, event_time_start, event_time_end):
    time = self._get_formatted_time(event_time_start, event_time_end)
    return Booking(event_name, time[0], time[1])

  def _get_formatted_time(self, event_time_start, event_time_end):
    start_date = self.now.today()
    end_date = self.now.today()
    start_time = self.now.strptime(event_time_start, '%I:%M%p')
    start_date_time = self.now.combine(start_date, start_time.time())

    end_time = self.now.strptime(event_time_end, '- %I:%M%p')
    end_date_time = self.now.combine(end_date, end_time.time())
    if start_date_time.hour >= 12 and end_date_time.hour <= 12:
      tomorrow = datetime.now() + timedelta(days=1)
      end_date_time = self.now.combine(tomorrow.date(), end_time.time())

    return (start_date_time, end_date_time)


