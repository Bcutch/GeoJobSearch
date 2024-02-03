import mysql.connector

#import ScrapingBot

db = mysql.connector.connect(host="localhost", user="root", passwd="root")#, database="setup")

mycursor = db.cursor()

mycursor.execute("show databases")

for i in mycursor:
    print(i)