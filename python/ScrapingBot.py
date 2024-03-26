import time
import json
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import os

# Sleep for 1 Minute So That Python doesn't try to connect to the selenium server before it is established
# time.sleep(60)
# Variable That Gets Number Of Pages Scraped
scrapedPages = 3
SCROLL_PAUSE_TIME = 2.5
# Empty Array To Store Dictionaries With Job Data
globalJobData = []


#######################
#   INDEED SCRAPING   #
#######################

#
# WARNING: THIS WILL TAKE A VERY LONG TIME approx 5-10 minutes per page
#

# Run by calling:
# scrapeIndeed(numPages:int, jobData:list, jobLimit:int = -1)
#
# jobData list will be filled with found jobs
# 
# upon calling this a chrome session will open (do not close this, it should close automatically when finished)
# and job data will be scraped. The urls found will then be opened one by one in this chrome window and scraped for data.
#
# scraping indeed here runs much faster than scraping linkedIn

def scrapeIndeed(numPages:int, jobData:list, jobLimit:int = -1, serverHostname:str = "selenium") -> None:
    """ Scrapes indeed Website and saves found jobs to jobData. Could not find field data but instead got company, 
    posting date, remoteness, salary, company, and description.

    Args:
        numPages (int): number of pages to scrape from indeed
        jobData (list): list of dictionaries that this function will fill
        limit (int): sets a limit for the number of job listings that will be scraped. If Below 0, will scrape with no limit. Defaults to -1.
        serverHostname (str): specifies the hostname of the server that the remote driver will execute on.

    Raises:
        ValueError: Input parameter to function was incorrect
    """
    
    if isinstance(jobData, list) is False: 
        raise ValueError("jobData type not a list")
    if numPages <= 0 or jobLimit == 0:   # should only scrape web if asked to scrap a positive non-zero number of pages
        raise ValueError("Parameters not allowing scraping")
    
    jobCount = 0        # counts number of job listings added to database
    
    # Launch Selenium Web Browser
    # set options
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")     # only allows fatal errors to appear, prevents needless spam
    
    # Loop for going through each page and getting all 15 jobs information
    for i in range(numPages):
        # Dynamic url that uses the other last query to change pages, increases by 20 everytime which is what brings you to a new page
        url = f"https://ca.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=1dbe12f243c824bf&start={i * 20}"
        
        # init driver
        # driver should be init within this loop so indeed doesn't stop scraping
        serverURL = "http://"+serverHostname+":4444/wd/hub" #selenium
        # init driver
        options = webdriver.ChromeOptions()
        options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Remote(command_executor=serverURL, options=options)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(20)    # raises error if page not found in 20 seconds
        # Open URL and wait for everything to load
        driver.get(url)
        # Get Dynamic url as page source for beautiufl soup to parse through the website
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Loop to go through each reference tag, and run the driver for that specific link so that you can get the active link
        for element in soup.find_all('a', class_="jcs-JobTitle"):
            time.sleep(0.5)
            href = element.get('href') # Get link that the a is referencing to 
            driver.get("https:///ca.indeed.com/" + href) # Launch new driver with dynamic link
            url = driver.current_url # Save the new url that opens as the link for our job title
            
            jobSoup = BeautifulSoup(driver.page_source, 'html.parser') # Creates a new soup "Driver" for current page to parse through
            
            header = jobSoup.find('h1', class_="jobsearch-JobInfoHeader-title")
            if header is not None: 
                title = header.find('span').text # Code to get job title for given url
            
            # location
            location = jobSoup.find('div', {'data-testid': 'inlineHeader-companyLocation'})
            if location is not None: 
                location = location.text
            
            # company
            company = jobSoup.find('div', class_='css-141snrz eu4oa1w0')
            if company is not None: 
                company = company.text
            
            # get additional info
            additional = jobSoup.find('div', id="salaryInfoAndJobType")
            salary = None
            jobType = None
            if additional is not None:
            # print(insights)
                salary = additional.find('span', class_="css-19j1a75 eu4oa1w0")
                if salary is not None: 
                    salary = salary.text
                jobType = additional.find('span', class_="css-k5flys eu4oa1w0")
                if jobType is not None: 
                    jobType = jobType.text
                if jobType is not None and jobType[:4] == ' -  ': 
                    jobType = jobType[4:]
            
            jobPostingDict = jobSoup.find('script', type="application/ld+json")
            
            postingdate = None
            if jobPostingDict is not None:
                jobPostingDict = json.loads(jobPostingDict.text)
                # convert to format yyyy-mm-dd
                postingdate = (jobPostingDict['datePosted'][0]+jobPostingDict['datePosted'][1] + jobPostingDict['datePosted'][2]+jobPostingDict['datePosted'][3] + '-'
                            + jobPostingDict['datePosted'][5]+jobPostingDict['datePosted'][6] + '-'
                            + jobPostingDict['datePosted'][8]+jobPostingDict['datePosted'][9])
                
                #description
                description = re.sub('<[^<]+?>', '', jobPostingDict.get('description', ''))
            
            #remoteness
            remote = jobSoup.find('div', 'css-6z8o9s eu4oa1w0')
            if remote is not None: 
                remote = remote.text
            remoteBool = not (remote == '')

            # add data to list
            jobData.append({'title': f'{title}', 'url': f'{url}', 'location':location,
                           'company':company, 'postingdate':f'{postingdate}', 'description': description,
                           'jobType':jobType, 'salary':salary, 'remote':remoteBool}) # Push to dictionary
            
            # increase job count and check for limit
            jobCount += 1
            if jobLimit > 0 and jobCount >= jobLimit:
                driver.quit()   # Close the browser window
                return

        driver.quit()   # Close the browser window
        
