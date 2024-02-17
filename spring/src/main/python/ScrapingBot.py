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


def scrapeLinkedIn(numPages:int, jobData:list):
    if numPages <= 0:   # should only scrape web if asked to scrap a positive non-zero number of pages
        return 
    linkedInUrl="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
    driver = webdriver.Chrome()
    # Open URL and wait for everything to load
    driver.get(linkedInUrl)
    driver.implicitly_wait(1)
    print(driver)

    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
    except Exception as error:  # failed to connect to URL
        print(error)
        raise ConnectionError
    pagesScraped = 0 #One page scraped equals one scroll to bottom due to infinite loading
    
    # Scrolls to bottom numPages times since linkedin uses infinite scrolling instead of pages

    
    while pagesScraped < numPages:
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
    # print(soup)
    driver.quit()
    
    # f = open('demofile.txt', "w", encoding="utf-8")
    # f.write(str(soup.find_all()))
    # f.close()

    # Loop to find all reference tags
    for jobListing in soup.find_all('div', class_='base-card'):
        title       = jobListing.find('span', class_='sr-only').text.strip() #title is printed with 3 new lines so use strip just to get title
        url         = jobListing.find('a', class_='base-card__full-link').get('href')
        location    = jobListing.find('span', class_="job-search-card__location").text.strip()
    #     # salary
    #     # field
    #     # remote
    #     # job type
        jobData.append({'title': f'{title}', 'url': f'{url}', 'location':f'{location}'}) # add to dictionary
        return
    
    # for element in soup.find_all():

tempData = []
scrapeLinkedIn(0, tempData)

for entry in tempData:
    print(entry)