import sys
import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="testdb")

mycursor = db.cursor()

def filter(filterBy, filterArg):

    retDict = []
    mycursor.execute("""SELECT * FROM job WHERE %s = '%s';""" % (filterBy, filterArg))

    for i in mycursor:
        retDict.append(i)

    return retDict