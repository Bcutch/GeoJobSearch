import time
from selenium import webdriver
from bs4 import BeautifulSoup

# Variable That Gets Number Of Pages Scraped
scrapedPages = 3

# Empty Array To Store Dictionaries With Job Data
jobData = []

# Loop for going through each page and getting all 15 jobs information
for i in range(scrapedPages):
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
        title = jobSoup.find('h1', class_="jobsearch-JobInfoHeader-title").find('span').text # Code to get job title for given url
        jobData.append({'title': f'{title}', 'url': f'{url}'}) # Push to dictionary

    driver.quit()   # Close the browser window

    #i = 0
    #for job in jobData:
    #    print(f'{i}: {job["title"]}: {job["url"]}')
    #    i+=1




