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
        assert (len(entry["title"])) > 0
        assert (len(entry["url"])) > 0

def testIndeedScraperNoPages() -> None:
    indeedData = []
    ScrapingBot.scrapeIndeed(numPages=0, jobData=indeedData)

    for entry in indeedData:
        assert (len(entry["title"])) == 0
        assert (len(entry["url"])) == 0

def testLinkedInScraper() -> None:
    # test that indeed scraper populates jobData
    linkedInData = []
    ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInData)

    for entry in linkedInData:      # test each possible entry that there is information found for each
        assert (len(entry["title"])) > 0
        assert (len(entry["url"])) > 0
        assert (len(entry["location"])) > 0

def testLinkedInScraperNoPages() -> None:
    linkedInData = []
    ScrapingBot.scrapeIndeed(numPages=0, jobData=linkedInData)

    assert len(linkedInData) == 0   # asked for no pages, shouldnt scrape any pages


def testLinkedInScraperNegativePages() -> None:
    linkedInData = []
    ScrapingBot.scrapeIndeed(numPages=-1, jobData=linkedInData)

    assert len(linkedInData) == 0   # asked for negative pages and this shouldnt be possible
