import mysql.connector
import re
import os
from pathlib import Path
    
# can be tested by running:
# pytest python/test_scraperToData.py


host = "mysql"                  # was "host"
user = "root"                   # was "root"
passwd = "pwd"                  # was "root"
databaseName = "template_db"    # was "testdb"
# host = "localhost"
# user = "root"
# passwd = "root"
# databaseName = "testdb"
tablename = "job"


class scraperToDataConnection:
    def __init__(self, host:str=host, user:str=user, passwd:str=passwd, databaseName:str=databaseName, tablename:str=tablename, 
                 dropTable:bool=False, debugFeedback:bool=False) -> None:
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
            resetTable:     WARNING: If True, will drop the current contents of the table. Defaults to False
            debugFeedback:  If True, print statements that could help debug will be displayed. Defaults to False
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
        self.databaseConnection = self.__connectDatabase(host=self.__host, user=self.__user, passwd=self.__passwd, database=self.databaseName)
        self.cursor = self.databaseConnection.cursor()     # init cursor
        
        # create table if not exists
        if self.dropTable and self.tableExists('job'): self.cursor.execute("DROP TABLE job")     # WARNING: DELETES TABLE TO RESET FOR TESTING PURPOSES
        self.createJobTable()
        
        

    def __del__(self) -> bool:
        """ Closes database connection once the class is terminated
        
        Returns:
            bool: True if successfully closed database connection, False if not successfully closed.
        """
        try:
            self.cursor.close()
            if self.debugFeedback: print(f"Cursor closed Successfully.")
            self.databaseConnection.close()
            if self.debugFeedback: print(f"Database: {self.databaseName} closed Successfully.")
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
        if self.databaseConnection != None: 
            buildString += f"Connected to Database: {self.databaseName}: {self.databaseConnection.is_connected()}\n"
        else:
            buildString += f"Connected to Database: {self.databaseName}: False\n"
        return buildString

    def __connectDatabase(self, host:str, user:str, passwd:str, database:str) -> mysql.connector.connection_cext.CMySQLConnection:
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
            conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            
            if self.debugFeedback: print(f"Database: {self.databaseName} successfully connected")
            return conn
        
        except Exception as error:
            if self.debugFeedback: print(error)
            raise ConnectionError   # table could not be connected to

    def tableExists(self, tablename:str=tablename) -> bool:
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
        
        if self.debugFeedback: print(f"{self.databaseName} existence={result}")
        
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
        
    
    def addJobData(self, jobData:list) -> bool:
        """Adds data from a list in the format: [{dict}, {dict}, {dict}...]. 
    Adds this data to the job sql table

    Returns:
        bool: Returns True if added the data successfully
    """
        for job in jobData:
            try:
                query = """INSERT INTO job
                           (title, company, location, description, url, salary, field, is_remote)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                values = [
                    job['title'],           # was job.get('title', None)        changed so that an error is thrown if no title is found
                    job.get('company', None),
                    job.get('location', None),
                    job.get('description', None),
                    job['url'],             # was job.get('url', None)        changed so that an error is thrown if no title is found
                    None,  # Placeholder for salary, will be calculated below
                    job.get('field', None),
                    int(job['remote']) if 'remote' in job else 0
                ]
            
                # Calculate and set salary
                if 'salary' in job and isinstance(job['salary'], str):
                    salaries = re.findall(r'[\$\£\€][,\d]+\.?\d*', job['salary'])
                    if len(salaries) > 0:
                        salary = round(sum(int(val[1:].replace(",", "")) for val in salaries) / len(salaries), 2)
                        values[5] = salary  # Set calculated salary
            
                self.cursor.execute(query, tuple(values))
                self.databaseConnection.commit()
            except mysql.connector.IntegrityError as error:
                if self.debugFeedback: print(error)
                if str(error)[:4] != "1062":
                    raise

        return True

        

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