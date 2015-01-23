""" 
This scrapes project URLs from Kickstarter projects page (the one with infinite scroll structure). 
The page is initially sorted by end date so that most recent projects are scraped first 

INPUT: None
OUTPUT: Kickstarter_recent_URLs.csv
DEPENDENCIES: xvfb or xvnc, Pyvirtualdisplay, Selenium, Firefox, python modules time and csv

Note: 
1. Run this code periodically to fetch latest project URLs
2. Add output URLs to composite list 
3. This file will output duplicated URLs (duplicated exactly once)
4. While adding to base URL list and de-duplicating, check for https:// v/s http://

File hosted on rosencrantz as Selenium_kickscraper.py
""" 

import time
import csv

# Importing virtual display
# Required for running Selenium on server without a display
from pyvirtualdisplay import Display

# Importing Selenium for emulating browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Starting a virtual display
display = Display(visible=0, size=(800,600))
display.start()

# Starting webdriver
# Only tested with Mozilla Firefox
browser = webdriver.Firefox()

## ----- TBD : Test if below speed-ups work --------------------

# Disabling images and flash for better performance
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def disableImages(self):
# get the Firefox profile object
    firefoxProfile = FirefoxProfile()
# Disable images
    firefoxProfile.set_preference('permissions.default.image', 2)
# Disable Flash
    firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
                                          'false')
# Set the modified profile while creating the browser object 
    self.browserHandle = webdriver.Firefox(firefoxProfile)

## ----- End of speed-ups ---------------------------------------

# Visit base URL
browser.get("https://www.kickstarter.com/discover/advanced?sort=end_date")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")
listoflinks = []

# A very high number will scrape all links
# However since we already have a list of old URLs only new URLs are needed
# Each additional page down will add approximately 20 extra URLs

no_of_pagedowns = 15000

# Before the first page down, a "Load more" button has to be clicked - Only once
browser.find_element_by_link_text("Load more").click()

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1

# For testing : Prints URLs in terminal
"""
post_elems = browser.find_elements_by_class_name("body")

for post in post_elems:
    print post.text
"""
# Comment out above block for a final run

links=browser.find_elements_by_tag_name('a')

# Insert URL list in output file
for i in links:
    if str(i.get_attribute('href'))[0:36] == "https://www.kickstarter.com/projects":
        listoflinks.append(i.get_attribute('href'))
        #print i.get_attribute('href')

myfile = open('Kickstarter_recent_URLs.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

for word in listoflinks:
    wr.writerow([word])

# Clean-up
browser.quit()
display.stop()