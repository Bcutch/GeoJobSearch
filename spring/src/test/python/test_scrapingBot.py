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
import pytest      # testing module
# path to file assumes pytest is run from the root directory (zenithProject)
import spring.src.main.python.ScrapingBot as ScrapingBot     # ScrapingBot.py 



# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

def testJobsExist() -> None:
    # check that jobData is not empty
    assert ScrapingBot.jobData != []

def testJobsHaveData() -> None:
    # for each entry in jobData including title and url, there is a non-zero value
    for entry in ScrapingBot.jobData:
        assert (len(entry["title"])) > 0
        assert (len(entry["url"])) > 0
    

