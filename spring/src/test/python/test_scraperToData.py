##
## NOTE: THE FILE MUST BE NAMED WITH test_ AT THE BEGINNING OR _test AT THE END
## PYTEST DOES NOT WORK IF THE FILE NAMES DO NOT INCLUDE EITHER OF THOSE
##

# how to test:
# --------------------------------------------------------
# cd to zenithProject directory
# type into the terminal: python -m pytest
# this will run all of the pytests in the project at once
# OPTIONAL: could also test by typing: python -m pytest --cov
#           this gives a much more in depth result with coverage
# --------------------------------------------------------
# requirements:
# pip install pytest
# OPTIONAL: pip install pytest-cov

# imports:
import pytest                               # testing module
from ...main.python import scraperToData      # scraperToData.py 
from ...main.python.scraperToData import scraperToDataConnection      # scraperToDataConnection class

# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

def testImproperHostname():
    improperHostname = "ja,s1f#a sh!/"    # assuming a hostname can't be the same name as this gibberish
    with pytest.raises(ConnectionError):
        scraperToDataConnection(host=improperHostname)
        
def testImproperUsername():
    improperUsername = "ja,s1f#a sh!/"    # assuming we won't be naming a username the same name as this gibberish
    with pytest.raises(ConnectionError):
        scraperToDataConnection(user=improperUsername)

def testImproperPasswd():
    improperPasswd = "ja,s1f#a sh!/"    # assuming we won't be naming a password the same name as this gibberish
    with pytest.raises(ConnectionError):
        scraperToDataConnection(passwd=improperPasswd)

def testImproperTablename():
    improperTablename = "ja,s1f#a sh!/"    # assuming we won't be naming a table the same name as this gibberish
    with pytest.raises(ConnectionError):
        scraperToDataConnection(databaseName=improperTablename)

def testDatabaseClosesProperly():
    connection = scraperToDataConnection()
    assert connection.__del__() == True     # closing the database must occur correctly

def testGetTablename():
    connection = scraperToDataConnection()
    assert connection.getDatabaseName() == connection.databaseName   # returned table name must be the same

def testTableCreated():
    connection = scraperToDataConnection()
    connection.createJobTable()
    assert connection.tableExists(f'{scraperToData.tablename}') == True        # tablename should exist 
    
def testAddCorruptData():
    with pytest.raises(LookupError):
        badData = [{'THIS':'IS A TEST'}]
        connection = scraperToDataConnection()
        connection.addJobData(badData)

def testAddMultipleData():
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':'THIS_IS_A_UNIT_TEST_TITLE',
        'url':'THIS_IS_FAKE_DATA'
        }]
    connection = scraperToDataConnection()
    connection.addJobData(data)     # we will add this same data multiple times to check for duplicates
    connection.addJobData(data)
    connection.addJobData(data)
    
    connection.cursor.execute(f"""
                              SELECT * FROM {scraperToData.tablename}
                              WHERE title = 'THIS_IS_A_UNIT_TEST_TITLE';
                              """)
    result = connection.cursor.fetchall()
    connection.cursor.clear_attributes()
    assert len(result) == 1      # there should not be any duplicate entries but there should be the one that was added
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    connection.cursor.clear_attributes()
    
# I made this before I realized we wouldn't be accessing the database like this
# Incase it needs to be implemented its here but I'm assuming we won't need it
# def testGetData():
#     data = [{   # this is fake data that will be inserted into the table and also removed
#         'title':'THIS_IS_A_UNIT_TEST_TITLE',
#         'url':'THIS_IS_FAKE_DATA'
#         }]
#     connection = scraperToDataConnection()
#     connection.addJobData(data)     # we will add this data to the table
    
#     retrievedData = connection.getData()
    
#     result = False
#     for entry in retrievedData:   # check if title exsits in result data and its formatted correctly
#         if entry['title'] == data[0]['title']: result = True
#     assert result == True       



#     connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
#     connection.database.commit()                # clear table of fake data
#     connection.cursor.clear_attributes()