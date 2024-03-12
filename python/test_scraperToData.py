##
## NOTE: THE FILE MUST BE NAMED WITH test_ AT THE BEGINNING OR _test AT THE END
## PYTEST DOES NOT WORK IF THE FILE NAMES DO NOT INCLUDE EITHER OF THOSE
##

# how to test:
# --------------------------------------------------------
# can be tested by running:
# pytest python/test_scraperToData.py
# or for coverage reports:
# pytest python/test_scraperToData.py --cov
# --------------------------------------------------------


# imports:
import pytest                               # testing module
import mysql.connector                      # sql
from scraperToData import scraperToDataConnection      # scraperToDataConnection class

# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

fakeDataTitle = 'THIS_IS_A_UNIT_TEST_TITLE'     # the title used for fake data when inserting it into the database
# this is important to know what to remove later
mockDbConn = None


@pytest.fixture()
def mockDatabase() -> scraperToDataConnection:
    mockDbConn = scraperToDataConnection(autoConnect=False)
    mockDbConn.databaseConnection = MagicMock()
    mockDbConn.cursor = MagicMock()
    
    return mockDbConn


@pytest.mark.parametrize("tablename,result,expected", 
    [("job", 1, True), ("userData", 0, False), (25, 0, False), (None, 0, False)]
)
def testTableExists(mockDatabase, tablename, result, expected):
    
    mockDatabase.cursor.configure_mock(
        **{
            "fetchone.return_value": [result]
        }
    )
    actual = mockDatabase.tableExists(tablename)
    assert actual == expected

@pytest.mark.parametrize("improperHostname", 
    [("a sentance"), (25), (None)]
)
def testImproperHostname(improperHostname):
    with pytest.raises(ConnectionError):
        scraperToDataConnection(host=improperHostname)

@pytest.mark.parametrize("improperUsername", 
    [("a sentance"), (25), (None)]
)   
def testImproperUsername(improperUsername):
    with pytest.raises(ConnectionError):
        scraperToDataConnection(user=improperUsername)

@pytest.mark.parametrize("improperPasswd", 
    [("a sentance"), (25), (None)]
)   
def testImproperPasswd(improperPasswd):
    with pytest.raises(ConnectionError):
        scraperToDataConnection(passwd=improperPasswd)

@pytest.mark.parametrize("improperdatabaseName", 
    [("a sentance"), (25), (None)]
)   
def testImproperdatabaseName(improperdatabaseName):
    with pytest.raises(ConnectionError):
        scraperToDataConnection(databaseName=improperdatabaseName)

def testDatabaseClosesProperly():
    connection = scraperToDataConnection(autoConnect=False)
    assert connection.__del__() == False     # no database active so it shouldnt close properly


@pytest.mark.parametrize("databaseName", 
    [("job"), ("mydatabase"), (25), (None)]
)  
def testGetDatabaseName(databaseName):
    conn = scraperToDataConnection(databaseName=databaseName, autoConnect=False)
    assert conn.getDatabaseName() == databaseName   # returned table name must be the same

@pytest.mark.parametrize("databaseName,result,expected", 
    [("job", 1, True), ("testdb", 0, False)]
)  
def testTableCreated(mockDatabase, databaseName,result,expected):
    mockDatabase.createJobTable()
    mockDatabase.cursor.configure_mock(
        **{
            "fetchone.return_value": [result]
        }
    )
    assert mockDatabase.tableExists(f'{databaseName}') == expected        # tablename should exist 
    
def testAddCorruptData(mockDatabase):
    badData = [{'THIS':'IS A TEST'}]
    
    with pytest.raises(KeyError):
        mockDatabase.addJobData(badData)

def testAddMultipleData(mockDatabase):
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
    assert mockDatabase.addJobData(data) == True     # we will add this same data multiple times to check for duplicates
    
    
def testLongUrlLength(mockDatabase):
    string = "a"*3000
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':string
        }]
    
    with pytest.raises(mysql.connector.DataError):
        mockDatabase.addJobData(data)                 # should not be able to add a value longer than the allowed length

    
def testNoTitle(mockDatabase): # title value MUST exist, if not an error should be raised
    data = [{   # this is fake data that will be inserted into the table and also removed
        'url':'THIS_IS_FAKE_DATA'
        }]
    
    with pytest.raises(KeyError):
        mockDatabase.addJobData(data)
    
    
    
def testNoURL(mockDatabase): # url value MUST exist, if not an error should be raised
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle
        }]
    
    with pytest.raises(KeyError):
        mockDatabase.addJobData(data)
    
    
    
def testAddWrongRemoteValue(mockDatabase):
    # remoteness should only be 0 or 1
    remoteData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'remote': "Hybrid"              # should be a bool, not string
        }]
    with pytest.raises(ValueError):
        mockDatabase.addJobData(remoteData)
    

def testAddCorrectRemoteValue(mockDatabase):
    # remoteness should add correctly
    
    remoteData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'remote': False              # should be a bool, not string
        }]
    assert mockDatabase.addJobData(remoteData) == True
    
    
def testHandleExtraData(mockDatabase):
    # should not add or try to add extra data if there is in the dictionary
    extraData = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        # assuming the following entries will never have a column in the database
        'cat': 'yes',
        'dog': 'no'
        }]
    assert mockDatabase.addJobData(extraData) == True            # should raise no errors
    
    
def testAddCorrectSalary(mockDatabase):
    # should add the correct salary value from the string
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'salary': 'around $150,000 per year'
        }]
    assert mockDatabase.addJobData(data) == True           # should raise no errors

    
def testAddNumericSalary(mockDatabase):
    # should add the correct salary value from the string
    data = [{   # this is fake data that will be inserted into the table and also removed
        'title':fakeDataTitle,
        'url':'THIS_IS_FAKE_DATA',
        'salary': 150_000
        }]
    assert mockDatabase.addJobData(data) == True            # should raise no errors
    
    
# # I made this before I realized we wouldn't be accessing the database like this
# # Incase it needs to be implemented its here but I'm assuming we won't need it
# # def testGetData():
# #     data = [{   # this is fake data that will be inserted into the table and also removed
# #         'title':fakeDataTitle,
# #         'url':'THIS_IS_FAKE_DATA'
# #         }]
# #     connection = scraperToDataConnection()
# #     connection.addJobData(data)     # we will add this data to the table
    
# #     retrievedData = connection.getData()
    
# #     result = False
# #     for entry in retrievedData:   # check if title exsits in result data and its formatted correctly
# #         if entry['title'] == data[0]['title']: result = True
# #     assert result == True       



# #     connection.cursor.execute(f"""DELETE FROM {connection.tablename} WHERE title='{data[0]['title']}'""")    
# #     connection.databaseConnection.commit()                # clear table of fake data


