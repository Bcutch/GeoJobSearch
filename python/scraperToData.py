import mysql.connector
from mysql.connector.connection import MySQLConnection
import re
from geopy.geocoders import Nominatim
    
# can be tested by running:
# pytest python/test_scraperToData.py


globalHost = "mysql"                  # was "host"
globalUser = "root"                   # was "root"
globalPasswd = "pwd"                  # was "root"
globalDatabaseName = "template_db"    # was "testdb"
# globalHost = "localhost"
# globalUser = "root"
# globalPasswd = "root"
# globalDatabaseName = "testdb"
globalTablename = "job"


class scraperToDataConnection:
    def __init__(self, host:str=globalHost, user:str=globalUser, passwd:str=globalPasswd, databaseName:str=globalDatabaseName, tablename:str=globalTablename, 
                 dropTable:bool=False, debugFeedback:bool=False, autoConnect:bool=True) -> None:
        """ Summary:
            Creates a connection within the class for a continous connection to the database.
            The connection will automatically close when the class is terminated at the end of a program.
            Data can continously be added using the addData() method for each time data is to be added.
            Data in the conncected database can be retrieved at any time using getData()
            
        Args:
            host:           hostname of the sql server that will be connected to
            user:           username of the sql server that will be connected to
            passwd:         password of the sql server that will be connected to
            databaseName:   name of the sql database that will be connected to
            dropTable:      WARNING: If True, will drop the current contents of the job table. Defaults to False
            debugFeedback:  If True, print statements that could help debug will be displayed. Defaults to False
            autoConnect:    If True, will automatically attempt to connect to the desired database. Defaults to True
        """
        # private variables
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        # public variables
        self.databaseName = databaseName
        self.tablename = tablename
        self.debugFeedback = debugFeedback
        self.dropTable = dropTable
        
        # create database connection
        self.databaseConnection = None
        self.cursor = None
        if autoConnect:
            self.databaseConnection = self.connectDatabase(host=self.__host, user=self.__user, passwd=self.__passwd, database=self.databaseName)
            self.cursor = self.databaseConnection.cursor()     # init cursor
        
        # create table if not exists
        if self.dropTable and self.tableExists(self.tablename):
            self.cursor.execute("DROP TABLE job")     # WARNING: DELETES TABLE TO RESET FOR TESTING PURPOSES
        if autoConnect:
            self.createJobTable()
        
        

    def __del__(self) -> bool:
        """ Closes database connection once the class is terminated
        
        Returns:
            bool: True if successfully closed database connection, False if not successfully closed.
        """
        try:
            self.cursor.close()
            if self.debugFeedback:
                print("Cursor closed Successfully.")
            self.databaseConnection.close()
            if self.debugFeedback:
                print(f"Database: {self.databaseName} closed Successfully.")
            return True
        except Exception as error:
            if self.debugFeedback:
                print(f"Database: {self.databaseName} or cursor could not be closed.")
                print(error)
            return False
    
    def __repr__(self) -> str:
        """ Combined the variables of the class together into the variable buildString

        Returns:
            str: buildString containing class information
        """
        buildString = "Class: scraperToDataConnection\n"
        buildString += "Variables:\n"
        buildString += f"\tdatabasename: {self.databaseName}\n"
        buildString += f"\tdebugFeedback: {self.debugFeedback}\n"
        buildString += "Summary:\n"
        if self.databaseConnection is not None: 
            buildString += f"Connected to Database: {self.databaseName}: {self.databaseConnection.is_connected()}\n"
        else:
            buildString += f"Connected to Database: {self.databaseName}: False\n"
        return buildString

    def connectDatabase(self, host:str, user:str, passwd:str, database:str) -> MySQLConnection:
        """ This function attempts to the connect to the sql sever based on the input parameters

        Args:
            host (str): hostname of the sql server that will be connected to
            user (str): username of the sql server that will be connected to
            passwd (str): password of the sql server that will be connected to
            database (str): name of the sql table that will be connected to

        Returns:
            bool: True if sql database was successfully connected, False if not connected
        """
        try:
            # conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            
            if self.debugFeedback: 
                print(f"Database: {self.databaseName} successfully connected")
            return conn
        
        except Exception as error:
            if self.debugFeedback:
                print(error)
            raise ConnectionError   # table could not be connected to

    def tableExists(self, tablename:str=globalTablename) -> bool:
        """ Checks if table exists in current schema.
            
        Returns:
            bool: True if table exists, False if table doesn't exist
        """
        self.cursor.execute(f"""SELECT EXISTS (
            SELECT *
            FROM information_schema.tables
            WHERE table_name = '{tablename}'
            );;""")           # select all tables with the name table name
        # {tablename}
        result = self.cursor.fetchone()[0] == 1  # check if table exists
        
        if self.debugFeedback: 
            print(f"{self.databaseName} existence={result}")
        
        return result                   # return result of if table exists
    
    def getDatabaseName(self) -> str:
        """ Retrieves name of database table used for this connection

        Returns:
            str: name of database table
        """
        return self.databaseName
    
    
    
    def createJobTable(self) -> None: 
        """ Creates sql table named job
        """
        if self.databaseName is None:
            raise ConnectionError(f"Aborted Connected. Attempted to create a table where databaseName={self.databaseName}")
        # had to decrease URL size from 2000 down to 768 to use url's as a
        # unique to to prevent duplicate entries
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS job (
            id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
            title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255),
            description TEXT,
            url VARCHAR(2083),                 
            salary INT,
            field VARCHAR(255),
            is_remote BOOLEAN  DEFAULT FALSE,
            latitude DECIMAL(11,8),
            longitude DECIMAL(11,8)
        );""")
        
        
    def __validateJobEntry(self, jobEntry:dict) -> bool:
        """ Attempts to validate if a job entry is valid to entry the database

        Args:
            jobEntry (dict): dictionary of a job entry

        Returns:
            int: true or false if job is valid or not
        """
        try:
            if self.jobExists(jobEntry) is True:
                # if job url already exists in database, skip job
                print("WARNING: Duplicate Entry Attempted")
                return False
            
            if len(jobEntry["url"]) > 2083: 
                print("WARNING: Caught URL Longer than allowed 2083 chars")
                
        except BaseException as error:
            print("WARNING in validating job entry:", error)
            return False
    
    def __parseSalary(self, salary:str) -> int:
        """ Parses salary field from string to int

        Args:
            salary (str): salary field as a string

        Returns:
            int: parsed salary
        """
        if salary is None:
            return None
        try:
            # Calculate and set salary
            salaries = re.findall(r'[\$\£\€][,\d]+\.?\d*', salary)
            if len(salaries) > 0:
                averageSalary = sum(float(val[1:].replace(",", "")) for val in salaries) / len(salaries)
                return round(averageSalary, 2)
                
        except BaseException as error:
            print("WARNING in parsing salary:", error)
        
        finally:
            return None
        
        
    def __calculateCoordinates(self, location:str, values:list) -> list:
        """ calculates long/lat coordinates from location

        Args:
            location (str): location field as a string

        Returns:
            list: [longitude, latitude]
        """
        if location is None:
            return [None, None]
        try:
            loc = Nominatim(user_agent="Geopy Library")
            getLoc = loc.geocode(location)
            if getLoc is not None: # Only set longitude and Latitude if a valid value is found for given location
                if len(values) < 10:  # Ensure that values has enough elements
                    values.extend([None] * (9 - len(values) + 1))
                longitude = getLoc.longitude
                latitude = getLoc.latitude
                print(f"Location: {location}, Longitude: {longitude}, Latitude: {latitude}")
                
                return [longitude, latitude]
                
        except BaseException as error:
            print("WARNING in calculating long/lat:", error)
        finally:
            return [None, None]
        
    def __addSingleJob(self, job:dict) -> bool:
        if self.__validateJobEntry(job) is False:
            # job was not valid
            return False
        
        try:
            query = """INSERT INTO job
                        (title, company, location, description, url, salary, field, is_remote, longitude, latitude)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            values = [
                job['title'],           # was job.get('title', None)        changed so that an error is thrown if no title is found
                job.get('company', None),
                job.get('location', None),
                job.get('description', None),
                job['url'],             # was job.get('url', None)        changed so that an error is thrown if no title is found
                None,  # Placeholder for salary, will be calculated below
                job.get('field', None),
                int(job['remote']) if 'remote' in job else 0,
                None,
                None
            ]
            # Calculate and set salary
            values[5] = self.__parseSalary(salary=job.get('salary'))
            # Use the Geopy library to get the longitude and latitude as long as a job has a location
            values[8], values[9] = self.__calculateCoordinates(location=job.get('location'), values=values)

            # update to database
            self.cursor.execute(query, tuple(values))
            self.databaseConnection.commit()
            
            return True
            
        except BaseException as error:
            print("WARNING:", error)
            return False
    
    def addJobData(self, jobData:list) -> int:
        """Adds data from a list in the format: [{dict}, {dict}, {dict}...]. 
        Adds this data to the job sql table

        Returns:
            int: Returns number of jobs added. This can be used to determine the percent of jobs that were successfully added.
        """
        if type(jobData) not in (dict, list):
            return 0
        
        if isinstance(jobData, dict):
            jobData = [jobData]
        
        totalJobsAdded = 0

        for jobEntry in jobData:
            if self.__addSingleJob(job=jobEntry) is True:
                totalJobsAdded += 1
            
        return totalJobsAdded

    def jobExists(self, jobEntry:dict):
        # if list attempt to change to dict
        if isinstance(jobEntry, list):
            jobEntry = jobEntry[0]
            
        try:
            if jobEntry['url'] is None:
                # job entry url shouldn't be none
                return False
            
            # count number of occurances of url parameter
            self.cursor.execute(f"""
                        SELECT COUNT(*)
                        FROM job 
                        WHERE url = '{jobEntry['url']}'
                        OR (
                            title = '{jobEntry['title']}'
                            AND company {f"= '{jobEntry.get('company')}'" if jobEntry.get('company') is not None else "is NULL"}
                            AND location {f"= '{jobEntry.get('location')}'" if jobEntry.get('location') is not None else "is NULL"}
                            );
                        """)

            count = self.cursor.fetchone()[0]
            return count > 0   # if number of occurances is greater than 0, url exists
        
        except TypeError as e:
            # there must've been something wrong with the inputs
            print(f"WARNING in {__name__} in jobUrlExists:", e)
            return False
        
        except KeyError as e:
            # there was probably no title or url in given job entry
            print(f"WARNING in {__name__} in jobUrlExists:", e)
            return False
        

# # I made this before I realized we wouldn't be accessing the database like this
# # Incase it needs to be implemented its here but I'm assuming we won't need it
#     def getData(self, tablename:str=tablename) -> list:
#         """ Returns all of the table data as a list of dictionaries in the mysql table

#         Args:
#             tablename (str, optional): name of the table to pull the data from. Defaults to 'job'.

#         Returns:
#             list: Returns all of the job data as a list of dictionaries in the mysql job table

#         """
#         # get list of tuples all job data
#         self.cursor.execute(f"""
#                     SELECT * FROM {tablename}
#                     """)
#         jobEntries = self.cursor.fetchall()
        
#         result = []
#         # convert list of tuples to list of dictionaries
#         for job in jobEntries:
#             tempDict = {}
#             tempDict.update({'id'            :job[0]})
#             tempDict.update({'title'         :job[1]})
#             tempDict.update({'company'       :job[2]})
#             tempDict.update({'location'      :job[3]})
#             tempDict.update({'description'   :job[4]})
#             tempDict.update({'salary'        :job[5]})
#             tempDict.update({'field'         :job[6]})
#             tempDict.update({'is_remote'     :job[7]})
#             tempDict.update({'latitude'      :job[8]})
#             tempDict.update({'longitude'     :job[9]})
            
#             result.append(tempDict.copy())      # add dictionary to result
#             tempDict.clear()
            
#         return result
        

# connection = scraperToDataConnection()
# jobData = []
# ScrapingBot.scrapeLinkedIn(1, jobData)
# connection.addJobData(jobData)


# sqlSetup = os.path.relpath('mysql\\scripts\\setup.sql')
# with open(sqlSetup, 'r') as sqlFile:
#     fileContents = sqlFile.read()
# print(fileContents)