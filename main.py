"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping indeed for job listings, grabbing certain items
"""
from selenium import webdriver

PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.youtube.com")
# Close closes a single table quit() will completely close all
print(driver.title)
driver.close()
