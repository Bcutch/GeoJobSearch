import mysql.connector
import re
    
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
# tablename = "job"


class scraperToDataConnection:
    def __init__(self, host:str=host, user:str=user, passwd:str=passwd, databaseName:str=databaseName, tablename:str=tablename, 
                 debugFeedback:bool=False) -> None:
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
            debugFeedback:  If true, print statements that could help debug will be displayed. Defaults to False
        """
        # private variables
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        # public variables
        self.databaseName = databaseName
        self.tablename = tablename
        self.debugFeedback = debugFeedback
        
        # create database connection
        self.database = self.__connectDatabase(host=self.__host, user=self.__user, passwd=self.__passwd, database=self.databaseName)
        self.cursor = self.database.cursor()     # init cursor
        
        # create table if not exists
        # if self.tableExists('job'): self.cursor.execute("DROP TABLE job")     # WARNING: DELETES TABLE TO RESET FOR TESTING PURPOSES
        self.createJobTable()
        
        

    def __del__(self) -> bool:
        """ Closes database connection once the class is terminated
        
        Returns:
            bool: True if successfully closed database connection, False if not successfully closed.
        """
        try:
            self.cursor.close()
            if self.debugFeedback: print(f"Cursor closed Successfully.")
            self.database.close()
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
        if self.database != None: 
            buildString += f"Connected to Database: {self.databaseName}: {self.database.is_connected()}\n"
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
            database = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
            
            if self.debugFeedback: print(f"Database: {self.databaseName} successfully connected")
            return database
        
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
            url VARCHAR(768) UNIQUE,                   
            salary INT,
            field VARCHAR(255),
            is_remote BOOLEAN  DEFAULT FALSE,
            latitude DECIMAL(11,8),
            longitude DECIMAL(11,8)
        );""")
        
    
    def addJobData(self, jobData:list) -> bool:
        """ Adds data from a list in the format: [{dict}, {dict}, {dict}...]. 
        Adds this data to the job sql table

        Returns:
            bool: Returns True if added the data successfully
        """
        for job in jobData:
            try:
                # title and url columns must have inforation or error will raise
                # all other fields can have null values
                buildString = """INSERT INTO job"""
                buildString += """ (title, company, location, description, url, salary, field, is_remote)"""
                buildString += """ VALUES ("""
                buildString += f""""{job['title']}","""
                buildString += f""""{job['company']}",""" if 'company' in job else """NULL,"""
                buildString += f""""{job['location']}",""" if 'location' in job else """NULL,"""
                buildString += f""""{job['description']}",""" if 'description' in job else """NULL,"""
                buildString += f""""{job['url']}","""

                salaryString = """NULL,"""
                if 'salary' in job: 
                    salaries = re.findall(r'[\$\£\€][,\d]+\.?\d*', job['salary'])       # uses regex to find all dollar values in string
                    if len(salaries) > 0: 
                        salary = round(sum(int(val[1:].replace(",","")) for val in salaries)/len(salaries), 2)  # take average and round to 2 decimal places
                        salaryString = f"""{salary},"""
    
                buildString += salaryString
                buildString += f""""{job['field']}",""" if 'field' in job else """NULL,"""
                buildString += f"""{int(job['remote'])}""" if 'remote' in job else """0"""
                buildString += """);"""
                
                self.cursor.execute(buildString)
                self.database.commit()  # commit insert to database
            except mysql.connector.IntegrityError as error:
                # duplicate entry was attempted if this runs
                if self.debugFeedback: print(error)
                if str(error)[:4] != "1062":         # mysql error code 1062 is for duplicate entry attempt in a unique column
                                                    # if not this error code then error is something else bad and error is re-raised.
                    raise mysql.connector.IntegrityError(error)
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

