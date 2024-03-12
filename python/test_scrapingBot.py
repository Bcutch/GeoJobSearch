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



# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent


# global testing variables
indeedJobData = []
linkedInJobData = []

# this function is run first and fills the arrays with scrapped data
@pytest.fixture(scope="session", autouse=True)
def setupScrapeData():
    serverPath = os.path.join(os.path.dirname(__file__), 'test/selenium-server-4.18.1.jar')
    # parent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
    with subprocess.Popen(['java', '-jar', serverPath, 'standalone'], 
                          stdout=subprocess.DEVNULL,    # prevents needless spam of stdout
                          stderr=subprocess.STDOUT) as process:
        
        endTime = time.time() + 10  # will end after a timeout of 10 seconds
        curTime = time.time()
        
        while process is None and curTime < endTime:
            curTime = time.time()   # waits for process to be not None or time happens
            
        ScrapingBot.scrapeIndeed(numPages=1, jobData=indeedJobData, jobLimit=10, serverHostname="localhost")
        # ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInJobData, jobLimit=10, serverHostname="localhost")
        
        yield
        process.kill()
        process.terminate()
        process.wait(5)
    
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


def testLinkedInScraperWorks() -> None:
    # test that indeed scraper populates jobData

    for entry in linkedInJobData:
        assert len(entry["title"]) > 0
        assert len(entry["url"]) > 0
        assert len(entry["company"]) > 0
        assert len(entry["description"]) > 0
        assert len(entry["location"]) > 0
        assert entry["remote"] in (True, False)
        assert "salary" in entry
        assert "jobType" in entry
        
 
def testIndeedScraperNoPages() -> None:
    emptyData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(0, emptyData)

def testLinkedInScraperNoPages() -> None:
    emptyData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(0, emptyData)
        
