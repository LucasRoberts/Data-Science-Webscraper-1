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
import time


def main():
    # Setting up Chromedriver
    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.set_window_size(1280, 720)

    # Grabbing Job Title
    user_input_job = input("Enter the job title: ").lower()
    user_input_job.replace(" ", "%20")
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={user_input_job}"
    driver.get(url)

    # Close closes a single table quit() will completely close all
    jobs = int(input("Enter how many jobs would you like to find: "))
    counter = 1
    running = True
    company_info = []

    # Check how many jobs are on the page after user inputted job title
    time.sleep(5)
    try:
        actual_jobs = driver.find_element_by_xpath("//div[@data-test='MainColSummary']/p[@data-test='jobsCount']").get_attribute("textContent")
        actual_jobs = int(actual_jobs.strip(" jobs"))
    except selenium.common.exceptions.NoSuchElementException:
        print("Failed to find the number of jobs on the site.")
        actual_jobs = 0

    # If there are no jobs, exits the program
    if actual_jobs == 0:
        print("You entered an incorrect job title or one with 0 job postings.\n Try searching another job title.")
        running = False
        driver.close()
    # If the jobs requested are more than the amount listed, lowers the amount requested to amount listed.
    elif jobs > actual_jobs:
        print("The amount of jobs you want are less than how many there are.")
        if input(f"Would you like to search {actual_jobs} instead?\n Enter 'yes' or 'no' to continue: ") == "yes":
            jobs = actual_jobs
        else:
            running = False

    # Get rid of the pop-up
    try:
        driver.find_element_by_class_name("react-job-listing").click()
        driver.find_element_by_class_name("modal_closeIcon-svg").click()
    except selenium.common.exceptions.NoSuchElementException:
        print("Failed to close pop up")
        running = False

    while running:
        for job_number in range(1, jobs+1, 1):
            print(job_number)

            # Grabs the company name
            try:
                company_name = driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[1]/a[1]/span").text
            except selenium.common.exceptions.NoSuchElementException:
                company_name = -1

            # Grabs the title of the job
            try:
                job_title = driver.find_element_by_xpath(f"//li[{counter}]/div[2]/a[1]/span").text
            except selenium.common.exceptions.NoSuchElementException:
                job_title = -1

            # Grabs the location of the job
            try:
                location = driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[2]/span").text
            except selenium.common.exceptions.NoSuchElementException:
                location = -1

            # Grabs how much the salary is
            try:
                pay = driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[3]/div[1]/span").text
            except selenium.common.exceptions.NoSuchElementException:
                pay = -1

            # Grabs how long the job has been up
            try:
                job_age = driver.find_element_by_xpath(f"//li[{counter}]/div[2]/div[3]/div[2]/div[2]").text
            except selenium.common.exceptions.NoSuchElementException:
                job_age = -1

            # Grabs the rating of the company x/5 stars
            try:
                rating = driver.find_element_by_xpath(f"//li[{counter}]/div[1]/span").text
            except selenium.common.exceptions.NoSuchElementException:
                rating = -1

            company_info.append({"Company Name": company_name.lower(),
                                 "Job Title": job_title.lower(),
                                 "Location": location.lower(),
                                 "Pay": pay.lower(),
                                 "Job Post Age": job_age.lower(),
                                 "Rating": rating.lower()
                                 })

            if counter == jobs:
                running = False
            elif counter == 30:
                # Clicks the next page button
                driver.find_element_by_xpath("//a[@data-test='pagination-next']").click()
                counter = 0
                # instead of doing the math this will just subtract the 30 jobs it just went through to determine
                # When to click the next page button
                jobs -= 30
                time.sleep(5)
            counter += 1
    print(company_info)
    driver.close()


if __name__ == "__main__":
    main()
