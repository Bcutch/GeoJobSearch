import time
from selenium import webdriver
from bs4 import BeautifulSoup

<<<<<<< HEAD
# Sleep for 1 Minute So That Python doesn't try to connect to the selenium server before it is established
=======
>>>>>>> 9d74044 (Fixed compose.yml issues)
time.sleep(60)
# Variable That Gets Number Of Pages Scraped
scrapedPages = 1
SCROLL_PAUSE_TIME = 2.5
# Empty Array To Store Dictionaries With Job Data
jobData = []
serverURL = "http://selenium:4444/wd/hub"

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Remote(command_executor=serverURL, options=options)


def scrapeIndeed(numPages, jobData, driver):
    # Loop for going through each page and getting all 15 jobs information
    for i in range(scrapedPages):
        # Dynamic url that uses the other last query to change pages, increases by 20 everytime which is what brings you to a new page
        url = f"https://ca.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=1dbe12f243c824bf&start={i * 20}"
        
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
            url = ("https:///ca.indeed.com/" + href) # Save the new url that opens as the link for our job title
            
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
            driver.quit()


def scrapeLinkedIn(numPages, jobData, driver):
    url="https://www.linkedin.com/jobs/search?position=1&pageNum=0"
    # Open URL and wait for everything to load
    driver.get(url)
    driver.implicitly_wait(10)

    last_height = driver.execute_script("return document.body.scrollHeight")
    pagesScraped = 0 #One page scraped equals one scroll to bottom due to infinite loading
    
    # Scrolls to bottom numPages times since linkedin uses infinite scrolling instead of pages

    
    while pagesScraped != numPages:
        pagesScraped+= 1
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
    driver.quit()
>>>>>>> 25c3fff (Python container created and script works for linked in, but when I try to run the container in the dev environment it won't work, only works when i run it as a seperate image)
=======
>>>>>>> 9d74044 (Fixed compose.yml issues)

    # Loop to find all reference tags
    for element in soup.find_all('a', class_="base-card__full-link"):
        title = element.find('span').text.strip() #title is printed with 3 new lines so use strip just to get title
        url = element.get('href')
        jobData.append({'title': f'{title}', 'url': f'{url}'}) # add to dictionary

scrapeIndeed(scrapedPages, jobData, driver)
# scrapeLinkedIn(scrapedPages, jobData, driver)

for element in jobData:
       print(f"{element['title']}: {element['url']}")

<<<<<<< HEAD
driver.quit()
=======
driver.quit()
>>>>>>> 9d74044 (Fixed compose.yml issues)
