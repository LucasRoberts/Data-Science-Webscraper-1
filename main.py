"""
Author: Lucas Roberts
Date: 9/30/21
Description: I will be scrapping Glassdoor for job listings, grabbing certain items
"""
import pandas as pd
import glassdoor_scrapper as scrapper

# Gets info
jobs = input("Enter the job title: ")
location = input("Enter the location or 'none': ")
num_jobs = input("How many jobs would you like to look for: ")


df = scrapper.scrapper(jobs=jobs, location=location, num_of_jobs=num_jobs)
print(df)
print(df.head)
df.to_csv("job_csv.csv")

# temp_df = pd.read_csv("job_csv.csv")
#
# writer = pd.ExcelWriter("Job_Data.xlsx")
#
# temp_df.to_excel(writer)
#
# writer.save()
