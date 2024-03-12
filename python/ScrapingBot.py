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
            location = jobSoup.find('div', class_='css-1ikmi61 eu4oa1w0')
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
        
        
# tempData = []
# scrapeIndeed(numPages=5, jobData=tempData)
# # print(tempData)
# f = open('indeedData.txt',"w", encoding="utf-8")
# for item in tempData:   
#     f.write(str(item)+'\n')
# f.close()
        
        
        
#########################
#   LINKEDIN SCRAPING   #
#########################

#
# WARNING: THIS WILL TAKE A VERY LONG TIME approx 5-10 minutes per page
#

# Run by calling:
# scrapeLinkedIn(numPages:int, jobData:list, jobLimit:int = -1)
#
# jobData list will be filled with found jobs
# 
# upon calling this a chrome session will open (do not close this, it should close automatically when finished)
# and job data will be scraped. The urls found will then be opened one by one in this chrome window and scraped for data.
#
# unfortunatly this cannot run much faster as if you scrape too fast, linkedIn will detect the scraping and temporarily
# refuse your the connection to linkedIn
# this code should be able to handle many of the errors however there are many many MANY possible ways this could go wrong.
# good luck
        


def getSoupforLinkedIn(url:str, driver:webdriver.Chrome, options:webdriver.ChromeOptions = None, numPages:int = 0) -> BeautifulSoup:
    """ This function takes in a driver, and url and will return the Beautiful soup for the
    associated linked in page if one is found. This is needed because LinkedIn will popup an 
    auth_wall sign in page after 3 quick consecutive searches. This function gets around this
    to ensure none of the data can be messed with.


    Args:
        url (str): linkedIn URL that will be searched
        driver (webdriver.Chrome): webdriver that will be used
        options (webdriver.ChromeOptions, optional): options class that will be used in the webdriver. Defaults to None.
        numPages (int, optional): number of pages, used to determine scroll height of page since linkedIn has endless scroll. Defaults to 0.

    Raises:
        ConnectionError: this is raised if cannot connect to linkedIn
        TimeoutError: This is raised if there is a timeout while scrapping linkedIn

    Returns:
        BeautifulSoup: Returns the BeautifulSoup class if found. Returns None if nothing is found
    """
    
    # variables
    soup = None             # final return variable to return soup
    _options = options
    if _options is None:                    # set options if none exist
        _options = webdriver.ChromeOptions()
        _options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
    maxTimeoutAttempts = 10        # number of attempts to be made before a timeout error is raised
    timeoutAttempts = 0         # number of attempts used before timeout
    sleepSecondsLoaded = 2         # number of seconds to wait after a page loaded successfully
    sleepSecondsAuth = 5            # number of seconds to wait after a page is auth wall
    pageKey = None                  # pagekey of loaded linkedIn page
    authWallPrefix = "auth_wall"        # prefix in scraped HTML that determines file is authentication wall
    
    try:
        # Open URL and wait for everything to load
        driver.get(url)
        time.sleep(sleepSecondsLoaded)
        
        #
        # if scrolling required, scroll
        #
        if numPages > 0:
            last_height = 0 
            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
            except Exception:  # failed to scroll
                # no scroll height
                last_height = -1
                raise ConnectionError("Failed to get last_height")
            pagesScraped = 0 #One page scraped equals one scroll to bottom due to infinite loading
            
            # Scrolls to bottom numPages times since linkedin uses infinite scrolling instead of pages
            while pagesScraped < numPages and last_height > -1:
                pagesScraped += 1
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        
        
        #
        #   loop until a not auth_wall page is found
        #
        while (pageKey is not None and pageKey[:len(authWallPrefix)] == authWallPrefix) or pageKey is None:    
            # if timeout, raise error
            if timeoutAttempts >= maxTimeoutAttempts:
                raise TimeoutError(f"Max timeouts attempts ({timeoutAttempts} of {maxTimeoutAttempts}) reached searching LinkedIn")
            timeoutAttempts += 1
                
            # get page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if soup is None: 
                raise ConnectionError("Could not find Soup for linkedIn")    # page not found

            # get page header info
            meta = soup.find('meta')
            pageKey = None
            if meta is not None: 
                pageKey = meta.get("content")
            
            # check for net error
            netError = soup.find('body', class_='neterror')     # if class is net error
            # check for load error
            bodyError = soup.find('body')      
            if bodyError is not None: 
                bodyError = str(bodyError) == "<body></body>"     # if body is empty

            # if net error or load error
            if netError is not None or bodyError is True: 
                #  reload driver
                driver.quit()
                driver = None
                time.sleep(1)
                
                driver = webdriver.Chrome(options=_options)
                driver.implicitly_wait(10)
                driver.set_page_load_timeout(20)    # raises error if page not found in 20 seconds
                time.sleep(1)
                driver.get(url)
                time.sleep(1)
                

            # continue until no auth_wall or timeout
            if pageKey is not None and pageKey[:len(authWallPrefix)] == authWallPrefix:
                driver.get(url)
                time.sleep(sleepSecondsAuth)
    
    except ConnectionRefusedError as cre:       # sometimes, linkedIn will directly refuse connection if scraping too much
        print(cre)
        print("LinkedIn Refused Connection, cannot get soup.")
    
    except Exception as Error:
        print(Error)
        raise ConnectionError("An Error occured while retrieving soup for linkedIn")
            
    return soup
    


def scrapeLinkedIn(numPages:int, jobData:list, jobLimit:int = -1, serverHostname:str = "selenium") -> None:
    """ Scrapes linkedin Website and saves found jobs to jobData

    Args:
        numPages (int): number of pages to scrape from linkedIn
        jobData (list): list of dictionaries that this function will fill
        limit (int): sets a limit for the number of job listings that will be scraped. If Below 0, will scrape with no limit. Defaults to -1.

    Raises:
        ConnectionError: if anything goes wrong connecting to linkedIn, this will be raised
        ModuleNotFoundError: if soup does not find anything, this will be raised
        RuntimeError: General error. if anything goes wrong, this will be raised
        ValueError: Input parameter to function was incorrect

    """
    if isinstance(jobData, list) is False: 
        raise ValueError("jobData type not a list")
    
    if numPages <= 0 or jobLimit == 0:   # should only scrape web if asked to scrap a positive non-zero number of pages
        raise ValueError("Parameters not allowing scraping")
    linkedInUrl="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
    
    serverURL = "http://"+serverHostname+":4444/wd/hub"
    # init driver
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor=serverURL, options=options) 

    driver.implicitly_wait(10)
    driver.set_page_load_timeout(20)    # raises error if page not found in 20 seconds
    
    # Open URL and wait for everything to load
        
    soup = getSoupforLinkedIn(url=linkedInUrl, driver=driver, options=options, numPages=numPages)
    if soup is None: 
        raise ConnectionError("Could not get any info for linkedIn")
    
    jobCount = 0
    try:
        # Loop to find all reference tags
        for jobListing in soup.find_all('div', class_='base-card'):
            if jobListing is None: 
                raise ModuleNotFoundError("jobListing should have been found")
            url = jobListing.find('a', class_='base-card__full-link').get('href')
            
            # get soup for more details info
            detailsSoup = getSoupforLinkedIn(url=url, options=options, driver=driver)
            if detailsSoup is None: 
                driver.quit()
                return jobData
            
            # scrap data
            title       = jobListing.find('h3', class_='base-search-card__title').text.strip() #title is printed with 3 new lines so use strip just to get title
            location     = jobListing.find('span', class_="job-search-card__location").text.strip()
            postingdate    = jobListing.find('time').get('datetime')       # gets date as format: yyyy-mm-dd
            company     = jobListing.find('h4', class_='base-search-card__subtitle').text.strip()
            
            # open details from job page to get more info
            coreInfo     = detailsSoup.find_all('li', class_="description__job-criteria-item")
            description  = detailsSoup.find('div', 'show-more-less-html__markup')
            if description is not None:
                description = str(description.text)
            else:
                description = None
            
            jobType = None
            field = None
            seniority = None
            for element in coreInfo:
                if element.find('h3', class_ = 'description__job-criteria-subheader').text.strip() == 'Employment type':
                    jobType = str(element.find('span', class_ = 'description__job-criteria-text').text.strip())
                    
                if element.find('h3', class_ = 'description__job-criteria-subheader').text.strip() == 'Job function':
                    field = str(element.find('span', class_ = 'description__job-criteria-text').text.strip())
                
                if element.find('h3', class_ = 'description__job-criteria-subheader').text.strip() == 'Seniority level':
                    seniority = str(element.find('span', class_ = 'description__job-criteria-text').text.strip())
            
            salary = detailsSoup.find('div', class_='salary')
            if salary is not None: 
                salary = str(salary.text)
            else:
                salary = None
            
            
        
            jobData.append({'title': f'{title}', 'url': f'{url}', 'company':f'{company}', 
                            'location':f'{location}', 'postingdate':f'{postingdate}',
                            'jobType':jobType, 'field':f'{field}', 'salary':salary,
                            'seniority':seniority, 'description':description}) # add to dictionary
            
            jobCount += 1
            if jobLimit > 0 and jobCount >= jobLimit:   # if jobLimit is not negative and job count has passed limit
                driver.quit()                       # stop scraping
                return
            
    except Exception as error:
        print(error)
        raise RuntimeError("An error occured while scraping LinkedIn")
    finally:
        driver.quit()

# jobDict = []
# scrapeIndeed(1, jobDict, jobLimit=10)

# for element in jobDict:
#     print(element['title'])

#     # db = mysql.connector.connect(
# host="mysql",  # Updated to the new host
# user="root",  # DB_USER
# passwd="pwd",  # DB_PASSWORD
# database="template_db"  # DB_DATABASE
# # )
# print('Entering Job Data...')

# connection = scraperToDataConnection(host="mysql", user="root", passwd="pwd", databaseName="template_db")
# print("connected to db")
# connection.addJobData(jobDict)

# print('Job Data Entered')
# mycursor = db.cursor()

# # mycursor.execute("DROP TABLE job")

# print('Creating Table')

# mycursor.execute("""CREATE TABLE IF NOT EXISTS job (
#     id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     company VARCHAR(255),
#     location VARCHAR(255),
#     description TEXT,
#     url VARCHAR(2000) NOT NULL,
#     salary INT,
#     field VARCHAR(255),
#     is_remote BOOLEAN NOT NULL DEFAULT FALSE,
#     latitude DECIMAL(11,8),
#     longitude DECIMAL(11,8)
# );""")

# print('table Created')


# for job in jobDict:
#     print(job)
#     mycursor.execute("""INSERT INTO job (title, url) VALUES ("%s", "%s");""" % (job['title'], job['url']))
#     db.commit()

# db.close()


