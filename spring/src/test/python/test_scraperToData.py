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
import mysql.connector                      # sql
from .....python import scraperToData      # scraperToData.py 
from .....python.scraperToData import scraperToDataConnection      # scraperToDataConnection class

# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

fakeDataTitle = 'THIS_IS_A_UNIT_TEST_TITLE'     # the title used for fake data when inserting it into the database
# this is important to know what to remove later

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

def testImproperdatabaseName():
    improperdatabaseName = "ja,s1f#a sh!/"    # assuming we won't be naming a table the same name as this gibberish
    with pytest.raises(ConnectionError):
        scraperToDataConnection(databaseName=improperdatabaseName)

def testDatabaseClosesProperly():
    connection = scraperToDataConnection()
    assert connection.__del__() == True     # closing the database must occur correctly

def testGetDatabaseName():
    connection = scraperToDataConnection()
    assert connection.getDatabaseName() == connection.databaseName   # returned table name must be the same

def testTableCreated():
    connection = scraperToDataConnection()
    connection.createJobTable()
    assert connection.tableExists(f'{scraperToData.tablename}') == True        # tablename should exist 
    
def testAddCorruptData():
    badData = [{'THIS':'IS A TEST'}]
    connection = scraperToDataConnection()
    
    with pytest.raises(KeyError):
        connection.addJobData(badData)

def testAddMultipleData():
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'company': 'Shark Hunters',
        'location': "Atlantis",
        'postingdate': "3020-12-31",
        'jobType': "Full-Time",
        'field': "Fishing",
        'salary': "$200,000 - $300,000 per year",
        'seniority': "High-level",
        'description': "The \tcraziest job you'll ever see!!\n\n."
        }]
    connection = scraperToDataConnection()
    connection.addJobData(data)     # we will add this same data multiple times to check for duplicates
    connection.addJobData(data)
    connection.addJobData(data)
    
    connection.cursor.execute(f"""
                              SELECT * FROM {scraperToData.tablename}
                              WHERE title = '{fakeDataTitle}';
                              """)
    result = connection.cursor.fetchall()
    assert len(result) == 1      # there should not be any duplicate entries but there should be the one that was added
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    
def testLongUrlLength():
    string = "a"*1000
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':string
        }]
    connection = scraperToDataConnection()
    
    with pytest.raises(mysql.connector.DataError):
        connection.addJobData(data)                 # should not be able to add a value longer than the allowed length

    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    
def testNoTitle(): # title value MUST exist, if not an error should be raised
    data = [{   # this is fake data that will be inserted into the table and also removed
        'url':'THIS_IS_FAKE_DATA'
        }]
    connection = scraperToDataConnection()
    
    with pytest.raises(KeyError):
        connection.addJobData(data)
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE url='{data[0]['url']}'""")    
    connection.database.commit()                # clear table of fake data
    
    
def testNoURL(): # url value MUST exist, if not an error should be raised
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle
        }]
    connection = scraperToDataConnection()
    
    with pytest.raises(KeyError):
        connection.addJobData(data)
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data

def testEmptyData():
    emptyData = []
    
    connection = scraperToDataConnection()
    # with pytest.raises(IndexError):
    connection.addJobData(emptyData)
    
    connection.cursor.execute(f"""
                              SELECT * FROM {scraperToData.tablename}
                              WHERE title = '{fakeDataTitle}';
                              """)
    result = connection.cursor.fetchall()
    assert len(result) == 0      # there should not be any entries
    
    if len(result) > 0:
        connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{emptyData[0]['title']}'""")    
        connection.database.commit()                # clear table of fake data
    
    
def testAddWrongRemoteValue():
    # remoteness should only be 0 or 1
    remoteData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'remote': "Hybrid"              # should be a bool, not string
        }]
    connection = scraperToDataConnection()
    with pytest.raises(ValueError):
        connection.addJobData(remoteData)
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{remoteData[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data

def testAddCorrectRemoteValue():
    # remoteness should add correctly
    
    remoteData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'remote': False              # should be a bool, not string
        }]
    connection = scraperToDataConnection()
    connection.addJobData(remoteData)
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{remoteData[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    
def testHandleExtraData():
    # should not add or try to add extra data if there is in the dictionary
    extraData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        # assuming the following entries will never have a column in the database
        'cat': 'yes',
        'dog': 'no'
        }]
    connection = scraperToDataConnection()
    connection.addJobData(extraData)            # should raise no errors
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{extraData[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    
def testAddCorrectSalary():
    # should add the correct salary value from the string
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'salary': 'around $150,000 per year'
        }]
    connection = scraperToDataConnection()
    connection.addJobData(data)            # should raise no errors
    
    connection.cursor.execute(f"""
                              SELECT * FROM {scraperToData.tablename}
                              WHERE title = '{fakeDataTitle}';
                              """)
    result = connection.cursor.fetchall()
    assert 150_000 in result[0]
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    

def testAddCorruptSalary():
    # should add the correct salary value from the string
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'salary': 'nothing'
        }]
    connection = scraperToDataConnection()
    connection.addJobData(data)            # should raise no errors
    
    connection.cursor.execute(f"""
                              SELECT * FROM {scraperToData.tablename}
                              WHERE title = '{fakeDataTitle}';
                              """)
    result = connection.cursor.fetchall()
    assert 'nothing' not in result[0]
    
    connection.cursor.execute(f"""DELETE FROM {scraperToData.tablename} WHERE title='{data[0]['title']}'""")    
    connection.database.commit()                # clear table of fake data
    
    
# I made this before I realized we wouldn't be accessing the database like this
# Incase it needs to be implemented its here but I'm assuming we won't need it
# def testGetData():
#     data = [{   # this is fake data that will be inserted into the table and also removed
#         'title':fakeDataTitle,
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


