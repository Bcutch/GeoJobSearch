import time
from selenium import webdriver
from bs4 import BeautifulSoup


# Variable That Gets Number Of Pages Scraped
scrapedPages = 3
SCROLL_PAUSE_TIME = 2.5
# Empty Array To Store Dictionaries With Job Data
globalJobData = []

def scrapeIndeed(numPages, jobData):
    # Loop for going through each page and getting all 15 jobs information
    for i in range(numPages):
        # Dynamic url that uses the other last query to change pages, increases by 20 everytime which is what brings you to a new page
        url = f"https://ca.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=1dbe12f243c824bf&start={i * 20}"
        
        # Launch Selenium Web Browser
        driver = webdriver.Chrome()
        # Open URL and wait for everything to load
        driver.get(url)
        driver.implicitly_wait(10)
        # Get Dynamic url as page source for beautiufl soup to parse through the website
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Loop to go through each reference tag, and run the driver for that specific link so that you can get the active link
        for element in soup.find_all('a', class_="jcs-JobTitle"):
            href = element.get('href') # Get link that the a is referencing to 
            driver.get("https:///ca.indeed.com/" + href) # Launch new driver with dynamic link
            url = driver.current_url # Save the new url that opens as the link for our job title
            
            jobSoup = BeautifulSoup(driver.page_source, 'html.parser') # Creates a new soup "Driver" for current page to parse through
            if jobSoup == None:     # if None return from BeautifulSoup then continue
                continue

            header = jobSoup.find('h1', class_="jobsearch-JobInfoHeader-title")
            if header == None:     # if None find from header then continue
                continue

            title = header.find('span').text # Code to get job title for given url
            if title == None:      # if title not found then continue
                continue
            jobData.append({'title': f'{title}', 'url': f'{url}'}) # Push to dictionary

        driver.quit()   # Close the browser window
        
        
        
#########################
#   LINKEDIN SCRAPING   #
#########################

#
# WARNING: THIS WILL TAKE A VERY LONG TIME approx 5-10 minutes per page
#

# Run by calling:
# scrapeLinkedIn(numPages:int, jobData:list)
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
    if _options == None:                    # set options if none exist
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
            except Exception as error:  # failed to scroll
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
        while (pageKey != None and pageKey[:len(authWallPrefix)] == authWallPrefix) or pageKey == None:    
            # if timeout, raise error
            if timeoutAttempts >= maxTimeoutAttempts:
                raise TimeoutError(f"Max timeouts attempts ({timeoutAttempts} of {maxTimeoutAttempts}) reached searching LinkedIn")
            timeoutAttempts += 1
                
            # get page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if soup == None: raise ConnectionError("Could not find Soup for linkedIn")    # page not found

            # get page header info
            meta = soup.find('meta')
            pageKey = None
            if meta != None: pageKey = meta.get("content")
            
            # check for net error
            netError = soup.find('body', class_='neterror')     # if class is net error
            # check for load error
            bodyError = soup.find('body')      
            if bodyError != None: bodyError = str(bodyError) == "<body></body>"     # if body is empty

            # if net error or load error
            if netError != None or bodyError == True: 
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
            if pageKey != None and pageKey[:len(authWallPrefix)] == authWallPrefix:
                driver.get(url)
                time.sleep(sleepSecondsAuth)
    
    except ConnectionRefusedError as cre:       # sometimes, linkedIn will directly refuse connection if scraping too much
        print(cre)
        print("LinkedIn Refused Connection, cannot get soup.")
    
    except Exception as Error:
        print(Error)
        raise ConnectionError("An Error occured while retrieving soup for linkedIn")
            
    return soup
    


def scrapeLinkedIn(numPages:int, jobData:list) -> None:
    """ Scrapes linkedin Website and saves found jobs to jobData

    Args:
        numPages (int): number of pages to scrape from linkedIn
        jobData (list): list of dictionaries that this function will fill

    Raises:
        ConnectionError: if anything goes wrong connecting to linkedIn, this will be raised
        ModuleNotFoundError: if soup does not find anything, this will be raised
        RuntimeError: General error. if anything goes wrong, this will be raised

    """
    if numPages <= 0:   # should only scrape web if asked to scrap a positive non-zero number of pages
        return 
    linkedInUrl="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
    
    # init driver
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(20)    # raises error if page not found in 20 seconds
    
    # Open URL and wait for everything to load
        
    soup = getSoupforLinkedIn(url=linkedInUrl, driver=driver, options=options, numPages=numPages)
    if soup == None: raise ConnectionError("Could not get any info for linkedIn")
    
    try:

        # Loop to find all reference tags
        for jobListing in soup.find_all('div', class_='base-card'):
            if jobListing == None: raise ModuleNotFoundError("jobListing should have been found")
            url = jobListing.find('a', class_='base-card__full-link').get('href')
            
            # get soup for more details info
            detailsSoup = getSoupforLinkedIn(url=url, options=options, driver=driver)
            if detailsSoup == None: 
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
            if description != None:
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
            if salary != None: 
                salary = str(salary.text)
            else:
                salary = None
            
            
        
            jobData.append({'title': f'{title}', 'url': f'{url}', 'company':f'{company}', 
                            'location':f'{location}', 'postingdate':f'{postingdate}',
                            'jobType':jobType, 'field':f'{field}', 'salary':salary,
                            'seniority':seniority, 'description':description}) # add to dictionary
    except Exception as error:
        raise RuntimeError("An error occured while scraping LinkedIn")
    finally:
        driver.quit()

# tempData = []

# scrapeLinkedIn(1,tempData)

