##
## NOTE: THE FILE MUST BE NAMED WITH test_ AT THE BEGINNING OR _test AT THE END
## PYTEST DOES NOT WORK IF THE FILE NAMES DO NOT INCLUDE EITHER OF THOSE
##

# how to test:
# --------------------------------------------------------
# cd to zenithProject directory
# type into the terminal: python -m pytest
# this will run all of the pytests in the project at once
# could also test by typing: python -m pytest --cov
# this gives a much more in depth result with coverage
# --------------------------------------------------------
# requirements:
# pip install pytest
# OPTIONAL: pip install pytest-cov


# imports:
import pytest                               # testing module
from ...main.python import ScrapingBot      # ScrapingBot.py 


# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

def testIndeedScraperWorks() -> None:
    # test that indeed scraper populates jobData
    indeedData = []
    ScrapingBot.scrapeIndeed(numPages=1, jobData=indeedData)

    for entry in indeedData:
        # these values should never be none
        assert (entry["title"])         != None
        assert (entry["url"])           != None
        assert (entry["company"])       != None
        assert (entry["location"])      != None
        assert (entry["postingdate"])   != None
        
        # these values should never be empty
        assert (entry["jobType"])       != ""
        assert (entry["salary"])        != ""
        assert (entry["description"])   != ""
        
        # remote is a bool, either true or false always
        assert ((entry["remote"])        == True or (entry["remote"]) == False)

def testIndeedScraperNoPages() -> None:
    indeedData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(numPages=0, jobData=indeedData)
    
def testIndeedScraperBadListInput() -> None:
    
    with pytest.raises(ValueError):
        linkedInData = 'this is a string'
        ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInData, jobLimit=5)
        
def testLinkedInScraperNegativePages() -> None:
    linkedInData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(numPages=-1, jobData=linkedInData)

        

def testLinkedInScraper() -> None:
    # test that indeed scraper populates jobData
    linkedInData = []
    ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInData, jobLimit=10)

    for entry in linkedInData:      # test each possible entry that there is information found for each
        # these should never be None
        assert (entry["title"])         != None
        assert (entry["url"])           != None
        assert (entry["company"])       != None
        assert (entry["location"])      != None
        assert (entry["postingdate"])   != None
        
        # no null values
        assert (entry["jobType"])       != "NULL"
        assert (entry["field"])         != "NULL"
        assert (entry["salary"])        != "NULL"
        assert (entry["seniority"])     != "NULL"
        assert (entry["description"])   != "NULL"
        
        # check that all str types have data
        if type(entry["title"])       == str: assert len(entry["title"])       > 0
        if type(entry["url"])         == str: assert len(entry["url"])         > 0
        if type(entry["company"])     == str: assert len(entry["company"])     > 0
        if type(entry["location"])    == str: assert len(entry["location"])    > 0
        if type(entry["postingdate"]) == str: assert len(entry["postingdate"]) > 0
        if type(entry["jobType"])     == str: assert len(entry["jobType"])     > 0
        if type(entry["field"])       == str: assert len(entry["field"])       > 0
        if type(entry["salary"])      == str: assert len(entry["salary"])      > 0
        if type(entry["seniority"])   == str: assert len(entry["seniority"])   > 0
        if type(entry["description"]) == str: assert len(entry["description"]) > 0
        
        
def testLinkedInScraperNoPages() -> None:
    
    linkedInData = []
    with pytest.raises(ValueError):     # asked for no pages, shouldnt scrape any pages
        ScrapingBot.scrapeLinkedIn(numPages=0, jobData=linkedInData, jobLimit=5)
    
def testLinkedInScraperBadListInput() -> None:
    
    with pytest.raises(ValueError):
        linkedInData = 'this is a string'
        ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInData, jobLimit=5)

def testLinkedInScraperNegativePages() -> None:
    linkedInData = []
    with pytest.raises(ValueError):
        ScrapingBot.scrapeLinkedIn(numPages=-1, jobData=linkedInData)

