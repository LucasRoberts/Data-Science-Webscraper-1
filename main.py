"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping indeed for job listings, grabbing certain items
"""
import sys

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
# jobs = input("How many jobs would you like to grab: ")
jobs = 20
counter = 1
running = True
company_name = []
job_title = []
location = []
pay = []
job_age = []

# Get rid of the pop-up
temp_elem = driver.find_element_by_class_name("react-job-listing")
temp_elem.click()
close_popup = driver.find_element_by_class_name("modal_closeIcon-svg")
close_popup.click()


while running:
    for job_number in range(1, jobs+1, 1):
        print(job_number)
        try:
            company_name.append(driver.find_element_by_xpath(f"//li[{job_number}]/div[2]/div[1]/a[1]/span").text)
        except selenium.common.exceptions.NoSuchElementException:
            company_name.append(-1)

        try:
            job_title.append(driver.find_element_by_xpath(f"//li[{job_number}]/div[2]/a[1]/span").text)
        except selenium.common.exceptions.NoSuchElementException:
            job_title.append(-1)

        try:
            location.append(driver.find_element_by_xpath(f"//li[{job_number}]/div[2]/div[2]/span").text)
        except selenium.common.exceptions.NoSuchElementException:
            location.append(-1)

        try:
            pay.append(driver.find_element_by_xpath(f"//li[{job_number}]/div[2]/div[3]/div[1]/span").text)
        except selenium.common.exceptions.NoSuchElementException:
            pay.append(-1)

        try:
            job_age.append(driver.find_element_by_xpath(f"//li[{job_number}]/div[2]/div[3]/div[2]/div[2]").text)
        except selenium.common.exceptions.NoSuchElementException:
            job_age.append(-1)

        counter += 1
        if counter == jobs:
            running = False
    print(company_name)
    print(job_title)
    print(location)
    print(pay)
    print(job_age)
sys.exit()
