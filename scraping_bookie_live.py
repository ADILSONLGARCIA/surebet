#import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#changing chromedriver default options
options = Options()
options.headless = True
options.add_argument('window-size=1920x1080') #Headless = True

web = 'https://sports.tipico.de/en/live/soccer'
path = '/Users/.../chromedriver' #introduce your file's path inside '...'

#execute chromedriver with edited options
driver = webd