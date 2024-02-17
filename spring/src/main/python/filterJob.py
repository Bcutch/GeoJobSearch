import sys
import mysql.connector

#must be changed to connect to the database you want to use
db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="testdb")

mycursor = db.cursor()

#function to be called to return the dict with filtered jobs
def filter(filterBy, filterArg):

    retDict = []
#select statement using arguments
    mycursor.execute("""SELECT * FROM job WHERE %s = '%s';""" % (filterBy, filterArg))

    for i in mycursor:
        retDict.append(i)

    return retDict