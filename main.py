"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping indeed for job listings, grabbing certain items
"""
import pandas
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Setting up Chromedriver
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Grabbing Job Title
user_input = input("Enter the job title").lower()
user_input.replace(" ", "%20")
URL = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={user_input}"
driver.get(URL)
# Close closes a single table quit() will completely close all

try:
    # company_name = driver.find_elements_by_css_selector(".job-search-key-l2wjgv e1n63ojh0 jobLink span")
    company_name = driver.find_element_by_xpath("//li[@class=react-job-listing css-bkasv9 eigr9kq0]/div[1]/div/a/span")
except selenium.common.exceptions.InvalidSelectorException:
    company_name = -1
print(company_name)
jobs = []
