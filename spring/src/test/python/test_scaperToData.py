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
import spring.src.main.python.scraperToData as scraperToData     # scraperToData.py 



# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

def testJobsExist() -> None:
    # there is data in the jobDict dictionary
    assert len(scraperToData.jobDict) > 0
    assert scraperToData.jobDict != None

def testDatabasehasData() -> None:
    # check data can be retrieved from database
    scraperToData.mycursor.execute("SELECT * FROM job")
    result = scraperToData.mycursor.fetchall()

    assert len(result) > 0

def testDatabase() -> None:
    # database loaded successfully
    assert scraperToData.db != None

    

