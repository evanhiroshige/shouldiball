from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def driver():
  DRIVER_PATH = '/Users/ehiroshige/dev/driver/chromedriver'
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(options=chrome_options, executable_path=DRIVER_PATH)
  driver.implicitly_wait(10)
  return driver