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



# imports:
import pytest                               # testing module
import ScrapingBot      # ScrapingBot.py 


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
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(0, indeedData)


def testLinkedInScraperWorks() -> None:
    # test that indeed scraper populates jobData
    linkedInData = []
    ScrapingBot.scrapeLinkedIn(numPages=1, jobData=linkedInData)

    for entry in linkedInData:
        assert (len(entry["title"])) > 0
        assert (len(entry["url"])) > 0

def testLinkedInScraperNoPages() -> None:
    linkedInData = []
    
    with pytest.raises(ValueError):
        ScrapingBot.scrapeIndeed(0, linkedInData)

