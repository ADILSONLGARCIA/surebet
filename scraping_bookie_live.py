#import libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#changing chromedriver default options
options = Options() # creates an instance of the Options class
options.headless = True # turns on the headless mode
#opens the windows in a customized size on the background
options.add_argument('window-size=1920x1080') #Headless = True


#represents the betting site’s URL,
# while path represents the chromedriver’s path in your computer
web = 'https://sports.tipico.de/en/live/soccer'
path = '/Users/.../chromedriver' #introduce your file's path inside '...'

#execute chromedriver with edited options
driver = webdriver.Chrome(path, options=options) #applies the changes we made in the chromedriver
driver.get(web) #opens the browser

#Make ChromeDriver click a button
#option 1
#makes the driver wait until the ‘ok button’ of the cookie banner is clickable. If this throws an error,
# then use ‘option 2’ instead. To get the Xpath, right-click on the ‘ok button’ and inspect as we did before for the dropdown menu
accept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_evidon-accept-button"]')))
#option 2
# time.sleep(2)
# accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')

#Initialize your storage
teams = []
x12 = []
btts = []
over_under = []
odds_events = []

#select values from dropdown (update 1)
#makes the driver wait some seconds until the dropdown menus are located
dropdowns = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'SportHeader-styles-drop-down')))

#selects dropdowns menus
first_dropdown = Select(dropdowns[0])
second_dropdown = Select(dropdowns[1])
third_dropdown = Select(dropdowns[2])

#one of the three dropdowns that contain betting markets
#selects an element inside the dropdown menu with the help of the betting market’s name.
first_dropdown.select_by_visible_text('Both Teams to Score') #update 'Both teams to score?' -> 'Both Teams to Score'
second_dropdown.select_by_visible_text('Over/Under')
third_dropdown.select_by_visible_text('3-Way')


#update 2
#Looking for live events 'Program_LIVE'
box = driver.find_element_by_xpath('//div[contains(@testid, "Program_UPCOMING")]') #updated - box represents
# the box that contains sports events. The site also contains upcoming events, which we don’t need for this analysis.
#Looking for 'sports titles'
sport_title = box.find_element_by_class_name('SportTitle-styles-sport') #updated


# update 3 (commented code not necesssary anymore)
# for sport in sport_title:
    # selecting only football
#     if sport.text == 'Football':
parent = sport_title.find_element_by_xpath('./..') #immediate parent node
# update 4 (+3 times .find_element_by_xpath('./..'))
grandparent = parent.find_element_by_xpath('./..').find_element_by_xpath('./..').find_element_by_xpath('./..').find_element_by_xpath('./..')
#3. empty groups
try:
    empty_groups = grandparent.find_elements_by_class_name('EventOddGroup-styles-empty-group')
    empty_events = [empty_group.find_element_by_xpath('./..') for empty_group in empty_groups[:]]
except:
    pass


#Looking for single row events
single_row_events = grandparent.find_elements_by_class_name('EventRow-styles-event-row')
#4 Remove empty events from single_row_events
try:
    empty_events
    single_row_events = [single_row_event for single_row_event in single_row_events if single_row_event not in empty_events]
except:
    pass


#Getting data
for match in single_row_events:
    #'odd_events'
    odds_event = match.find_elements_by_class_name('EventOddGroup-styles-odd-groups')
    odds_events.append(odds_event)
    # Team names
    for team in match.find_elements_by_class_name('EventTeams-styles-titles'):
        teams.append(team.text)
#Getting data: the odds
for odds_event in odds_events:
    for n, box in enumerate(odds_event):
        rows = box.find_elements_by_xpath('.//*')
        if n == 0:
            x12.append(rows[0].text)
        #5 over/under + goal line
        if n == 1:
            parent = box.find_element_by_xpath('./..')
            goals = parent.find_element_by_class_name('EventOddGroup-styles-fixed-param-text').text
            over_under.append(goals+'\n'+rows[0].text)
            #6 both teams to score
            if n == 2:
                btts.append(rows[0].text)

driver.quit()


import pandas as pd
import pickle

#7 #unlimited columns
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Storing lists within dictionary
dict_gambling = {'Teams': teams, 'btts': btts,
                 'Over/Under': over_under, '3-way': x12}
#Presenting data in dataframe
df_tipico = pd.DataFrame.from_dict(dict_gambling)
#clean leading and trailing whitespaces of all odds
df_tipico = df_tipico.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#Save data with Pickle
output = open('df_tipico', 'wb')
pickle.dump(df_tipico, output)
output.close()
print(df_tipico)
