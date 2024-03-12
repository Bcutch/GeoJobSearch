##
## NOTE: THE FILE MUST BE NAMED WITH test_ AT THE BEGINNING OR _test AT THE END
## PYTEST DOES NOT WORK IF THE FILE NAMES DO NOT INCLUDE EITHER OF THOSE
##

# how to test:
# --------------------------------------------------------
# can be tested by running:
# pytest python/test_scrapingBot.py
# or for coverage reports:
# pytest python/test_scrapingBot.py --cov
# --------------------------------------------------------
# requirements:
# pip install pytest
# pip install pytest-cov



# imports:
import pytest                               # testing module
import ScrapingBot      # ScrapingBot.py 
import subprocess
import os
import time
from selenium import webdriver
import jsonToList
import urllib3.exceptions



# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent


# global testing variables
indeedJobData = []
linkedInJobData = []

# this function is run first and fills the arrays with scrapped data
@pytest.fixture(scope="session", autouse=True)
def setupScrapeIndeedData():
    global indeedJobData
    # global linkedInJobData
    
    serverPath = os.path.join(os.path.dirname(__file__), 'test/selenium-server-4.18.1.jar')
    process = subprocess.Popen(['java', '-jar', serverPath, 'standalone'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
    endTime = time.time() + 5  # will end after a timeout of 5 seconds
    curTime = time.time()
    
    while process is None and curTime < endTime:
        curTime = time.time()   # waits for process to be not None or time happens
        
    if curTime >= endTime:  # timeout connecting to selenium server occured
        indeedJobData = jsonToList.getSavedJobsIndeed()
        # linkedInJobData = jsonToList.getSavedJobsLinkedIn()
    else:
        ScrapingBot.scrapeIndeed(numPages=1, jobData=indeedJobData, jobLimit=10, serverHostname="localhost")
        # ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInJobData, jobLimit=1, serverHostname="localhost")
    
    # yield
    if process is not None:
        process.kill()
        process.terminate()
        process.wait(5)
        
        

def testJsonListTestDoubles():
    jobs = jsonToList.getSavedJobListings()
    assert len(jobs) > 0
    
def testJsonListSortedTestDoubles():
    indeedJobs = jsonToList.getSavedJobsIndeed()
    linkedInJobs = jsonToList.getSavedJobsLinkedIn()
    assert len(indeedJobs) > 0
    assert len(linkedInJobs) > 0

def testIndeedScraperWorks() -> None:
    # test that indeed scraper populates jobData

    for entry in indeedJobData:
        assert len(entry["title"]) > 0
        assert len(entry["url"]) > 0
        assert "company" in entry
        assert len(entry["description"]) > 0
        assert entry["remote"] in (True, False)
        assert "salary" in entry
        assert "location" in entry
        assert "jobType" in entry


# def testLinkedInScraperWorks() -> None:
#     # test that indeed scraper populates jobData

#     for entry in linkedInJobData:
#         assert len(entry["title"]) > 0
#         assert len(entry["url"]) > 0
#         assert len(entry["company"]) > 0
#         assert len(entry["description"]) > 0
#         assert len(entry["location"]) > 0
#         assert "salary" in entry
#         assert "jobType" in entry
        
 
def testIndeedScraperNoPages() -> None:
    emptyData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(0, emptyData)

# def testLinkedInScraperNoPages() -> None:
#     emptyData = []
#     with pytest.raises(ValueError):
#         ScrapingBot.scrapeLinkedIn(0, emptyData)
        
        
# def testGetSoupForLinkedInBadURL():
#     options = webdriver.ChromeOptions()
#     options.add_argument('log-level=3')     # only allows fatal errors to appear, prevents needless spam
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = None
    
#     try:
#         driver = webdriver.Chrome(options=options)
#         driver.implicitly_wait(10)
#         driver.set_page_load_timeout(20)    # raises error if page not found in 20 seconds
#     except urllib3.exceptions.MaxRetryError:
#         pass
        
            
#     badurl = "google.google"
#     with pytest.raises(ConnectionError):
#         ScrapingBot.getSoupforLinkedIn(url=badurl, driver=driver, options=options)
#     if driver is not None:
#         driver.close()
#         driver.quit()
        
