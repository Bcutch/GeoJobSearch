
# This is the script that is called from the docker file and will run every time
# docker compose is called
# imports
import ScrapingBot
import scraperToData
import time

# Sleep for 1 Minute So That Python doesn't try to connect to the selenium server before it is established
time.sleep(60)

# scrape 10 jobs off of indeed
jobDict = []
ScrapingBot.scrapeIndeed(1, jobDict, jobLimit=10)

# display jobs for testing purposes
for element in jobDict:
    print(element['title'])
    
# connect to mySQL job table
connection = scraperToData.scraperToDataConnection(host="mysql", user="root", passwd="pwd", databaseName="template_db")
print("connected to db")

# add jobs to table
numJobsAdded = connection.addJobData(jobDict)
print(f"Added {numJobsAdded}/{len(jobDict)} jobs")