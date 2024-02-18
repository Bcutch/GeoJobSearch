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
        


def getSoupforLinkedIn(url:str, iterations:int=0) -> BeautifulSoup:
    """ This function takes in a driver, and url and will return the Beautiful soup for the
    associated linked in page if one is found. This is needed because LinkedIn will popup an 
    auth_wall sign in page after 3 quick consecutive searches. This function gets around this
    to ensure none of the data can be messed with.

    Args:
        url (str): URL that will be searched

    Returns:
        BeautifulSoup: Returns the BeautifulSoup class if found. Returns None if nothing is found
    """
    # Open URL and wait for everything to load
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2)
    time.sleep(3)
    driver.refresh()
    
    soup = None
    
    timeout = 10
    while iterations < timeout:     # loop until a none auth_wall page is found
        
        # get page
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        if soup == None: return None    # page not found
        # print(soup)

        # if page is auth_wall, refresh
        meta = soup.find('meta')
        if meta != None: pageKey = meta.get("content")

        # continue refresh until no auth_wall
        if pageKey != None and pageKey[:9] == "auth_wall":
            driver.quit()
            # driver.implicitly_wait(1)
            time.sleep(1)
            return getSoupforLinkedIn(url, iterations + 1)
            

            
        else:
            break
    # print("start")
    # for item in driver.get_cookies():
    #     print(item)
    # print("end")
    # if timeout reached, raise error
    if timeout <= iterations:
        raise TimeoutError("Could not get pass LinkedIn Authentication Login Wall")
        
    
    return soup
    


def scrapeLinkedIn(numPages:int, jobData:list):
    if numPages <= 0:   # should only scrape web if asked to scrap a positive non-zero number of pages
        return 
    linkedInUrl="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
    driver = webdriver.Chrome()
    # Open URL and wait for everything to load
    driver.get(linkedInUrl)
    driver.implicitly_wait(1)
    print(driver)

    last_height = 0 
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
    except Exception as error:  # failed to connect to URL
        # no scroll height
        last_height = -1
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

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    # print(type(soup))
    # print(soup)
    driver.quit()
    
    # f = open('demofile.txt', "w", encoding="utf-8")
    # f.write(str(soup.find_all()))
    # f.close()
    # detailsDriver = webdriver.Chrome()
    
    count = 0
    limit = 3

    # Loop to find all reference tags
    for jobListing in soup.find_all('div', class_='base-card'):
        url = jobListing.find('a', class_='base-card__full-link').get('href')
        # currentJobId= jobListing.get('data-entity-urn').split(":")[-1]

        # locaiton yes
        # salary
        # field
        # remote
        # job type
        
        # must open page to find more information
        # Open URL and wait for everything to load
        # currentJobIdUrl = "https://www.linkedin.com/jobs/search?currentJobId="
        # detailsDriver.get(currentJobIdUrl+currentJobId)
        
        # print(f"link: {currentJobIdUrl+currentJobId}")
        

        # get soup for more details info
        detailsSoup = getSoupforLinkedIn(url)
        
        # scrap data
        title       = jobListing.find('h3', class_='base-search-card__title').text.strip() #title is printed with 3 new lines so use strip just to get title
        location     = jobListing.find('span', class_="job-search-card__location").text.strip()
        dateTime    = jobListing.find('time').get('datetime')       # gets date as format: yyyy-mm-dd
        company     = jobListing.find('h4', class_='base-search-card__subtitle').text.strip()
        # topcard       = detailsSoup.find('div', class_="topcard__flavor-row")
        # if topcard != None: place = topcard.find('a', class_="topcard__org-name-link")
        # if place != None:   location = place.text.strip() + ', ' + location
        coreInfo     = detailsSoup.find_all('li', class_="description__job-criteria-item")
        
        jobType = None
        field = None
        for element in coreInfo:
            # print(element)
            # print()
            if element.find('h3', class_ = 'description__job-criteria-subheader').text.strip() == 'Employment type':
                jobType = element.find('span', class_ = 'description__job-criteria-text').text.strip()
                
            if element.find('h3', class_ = 'description__job-criteria-subheader').text.strip() == 'Job function':
                field = element.find('span', class_ = 'description__job-criteria-text').text.strip()
        
        salary = detailsSoup.find('div', class_='salary')
        if salary != None: 
            salary = salary.text.strip()
        else:
            salary = 'NULL'
            
            
        # print(salary)
                
        

        # print(coreInfo)
        
        # f = open('demofileDetails.txt', "w", encoding="utf-8")
        # f.write(str(detailsSoup.find_all()))
        # f.close()
        # time.sleep(3)
        
    
        jobData.append({'title': f'{title}', 'url': f'{url}', 'company':f'{company}', 
                        'location':f'{location}', 'dateTime':f'{dateTime}',
                        'jobType':f'{jobType}', 'field':f'{field}', 'salary':f'{salary}'}) # add to dictionary
        count += 1
        if count == limit: break
        
        # return
    

# tempData = []
# testlinkedInUrl="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
# # testdriver = webdriver.Chrome()
# # testdriver.quit()


# scrapeLinkedIn(1,tempData)

# for entry in tempData:
#     print(entry)