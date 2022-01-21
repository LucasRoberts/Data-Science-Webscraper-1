"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping Glassdoor for job listings, grabbing certain items
"""
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


def scrapper(jobs, location, num_of_jobs):
    """
    A scrapper for Glassdoor. Takes in 3 params and returns a Pandas DataFrame of
        Company Name, Job Title, Location, Pay, Job Age, Rating, Employee Count,
        Company Age, Company Type, Industry, Sector, Revenue, and Description
    :param jobs: int
    :param location: String
    :param num_of_jobs: int
    :return: Pandas DataFrame
    """
    # Initializing several variables
    counter = 1
    running = True
    company_info = []

    # Setting up Chromedriver
    path = "chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.set_window_size(1280, 720)

    # Grabbing Job Title
    user_input_job = jobs.lower()
    user_input_job.replace(" ", "%20")

    # Grabbing job Location if they want one if not enter 'none'
    user_input_loc = location.lower()
    if user_input_loc == "none":
        no_loc = True
    else:
        no_loc = False

    # Gets the url
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={user_input_job}"
    driver.get(url)

    # If there is a location clicks on the searchbar, types in location, and enters
    if not no_loc:
        try:
            search_button = driver.find_element(By.XPATH, "//input[@data-test='search-bar-location-input']")
            search_button.clear()
            search_button.send_keys(user_input_loc)
            search_button.send_keys(Keys.ENTER)
        except selenium.common.exceptions.NoSuchElementException:
            print("Failed to click on the location search bar.")
            running = False

    # Grabbing the amount of jobs
    try:
        jobs = int(num_of_jobs)
        if jobs == 0:
            print(f"jobs = {jobs}: This will cause false error downstream.")
            running = False
    except TypeError:
        print("You entered in the incorrect type for jobs. The required type is 'int'.")
        running = False
        jobs = 0

    print("\n")

    # Check how many jobs are on the page after user inputted job title
    time.sleep(5)
    try:
        actual_jobs = driver.find_element(By.XPATH, "//div[@data-test='MainColSummary']/p[@data-test='jobsCount']").get_attribute("textContent")
        actual_jobs = int(actual_jobs.strip(" jobs"))
    except selenium.common.exceptions.NoSuchElementException:
        print("Failed to find the number of jobs on the site.")
        actual_jobs = 0

    # If there are no jobs, exits the program
    if actual_jobs == 0 and running:
        print("You entered an incorrect job title or one with 0 job postings.\n Try searching another job title.")
        running = False

    # If the jobs requested are more than the amount listed, lowers the amount requested to amount listed.
    elif jobs > actual_jobs:
        print("The amount of jobs you want are less than how many there are.")
        if input(f"Would you like to search {actual_jobs} instead?\n Enter 'yes' or 'no' to continue: ") == "yes":
            jobs = actual_jobs
        else:
            running = False

    # Get rid of the pop-up
    try:
        driver.find_element(By.CLASS_NAME, "react-job-listing").click()
        driver.find_element(By.CLASS_NAME, "modal_closeIcon-svg").click()
    except selenium.common.exceptions.NoSuchElementException:
        print("Failed to close pop up")
        running = False

    # If running = False was triggered above this will print out the program is terminating
    if not running:
        print("Program is terminating...")
        driver.close()
    else:
        while running:
            tracker_for_jobs = jobs
            for job_number in range(1, jobs+1, 1):
                try:
                    driver.find_element(By.XPATH, f"//li[{counter}]/div[2]").click()
                    print(f"Progress: ({job_number}/{tracker_for_jobs})")

                    # Grabs the company name
                    try:
                        company_name = driver.find_element(By.XPATH, f"//li[{counter}]/div[2]/div[1]/a[1]/span").text
                    except selenium.common.exceptions.NoSuchElementException:
                        company_name = -1

                    # Grabs the title of the job
                    try:
                        job_title = driver.find_element(By.XPATH, f"//li[{counter}]/div[2]/a[1]/span").text
                    except selenium.common.exceptions.NoSuchElementException:
                        job_title = -1

                    # Grabs the location of the job
                    try:
                        location = driver.find_element(By.XPATH, f"//li[{counter}]/div[2]/div[2]/span").text
                    except selenium.common.exceptions.NoSuchElementException:
                        location = -1

                    # Grabs how much the salary is
                    try:
                        pay = driver.find_element(By.XPATH, f"//li[{counter}]/div[2]/div[3]/div[1]/span").text
                    except selenium.common.exceptions.NoSuchElementException:
                        pay = -1

                    # Grabs how long the job has been up
                    try:
                        job_age = driver.find_element(By.XPATH, f"//li[{counter}]/div[2]/div[3]/div[2]/div[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        job_age = -1

                    # Grabs the rating of the company x/5 stars
                    try:
                        rating = driver.find_element(By.XPATH, f"//li[{counter}]/div[1]/span").text
                        if rating == "":
                            rating = -1
                    except selenium.common.exceptions.NoSuchElementException:
                        rating = -1

                    time.sleep(1)

                    # These elements are grabbed from the inside of the right panel body
                    # Grabs the size of the company in terms of employees
                    try:
                        employees = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[1]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        employees = -1

                    # Grabs when the company was founded
                    try:
                        company_age = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[2]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        company_age = -1

                    # Grabs whether the company is public or private
                    try:
                        company_type = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[3]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        company_type = -1

                    # Grabs the industry the company operates in
                    try:
                        industry = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[4]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        industry = -1

                    # Grabs what sector the company is in
                    try:
                        sector = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[5]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        sector = -1

                    # Grabs the revenue of the company
                    try:
                        revenue = driver.find_element(By.XPATH, "//div[@id='EmpBasicInfo']/div[1]/div[1]/div[6]/span[2]").text
                    except selenium.common.exceptions.NoSuchElementException:
                        revenue = -1

                    # Grabs the description provided by the company
                    try:
                        description = driver.find_element(By.XPATH, "//div[@class='jobDescriptionContent desc']").text
                    except selenium.common.exceptions.NoSuchElementException:
                        description = -1

                except selenium.common.exceptions.NoSuchElementException:
                    company_name = -1
                    job_title = -1
                    location = -1
                    pay = -1
                    job_age = -1
                    rating = -1
                    employees = -1
                    company_age = -1
                    company_type = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    description = -1

                company_info.append({"Company Name": company_name,
                                     "Job Title": job_title,
                                     "Location": location,
                                     "Pay": pay,
                                     "Job Post Age": job_age,
                                     "Rating": rating,
                                     "Employees": employees,
                                     "Company Age": company_age,
                                     "Company Type": company_type,
                                     "Industry": industry,
                                     "Sector": sector,
                                     "Revenue": revenue,
                                     "Description": description
                                     })

                if counter == jobs:
                    running = False
                elif counter == 30:
                    # Clicks the next page button
                    driver.find_element(By.XPATH, "//button[@class='nextButton css-1hq9k8 e13qs2071']").click()
                    counter = 0
                    # instead of doing the math this will just subtract the
                    # 30 jobs it just went through to determine
                    # When to click the next page button
                    jobs -= 30
                    time.sleep(5)
                counter += 1

        driver.close()
        return pd.DataFrame(company_info)
