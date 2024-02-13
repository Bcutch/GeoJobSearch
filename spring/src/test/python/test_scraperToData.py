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
import mysql.connector                      # mysql needed in this file for testing

# TODO: when the database is created, change the database name from 'testdb' to the new name
databaseName = "testdb"

# tests:
# these functions don't have any naming restrictions from pytest
# they are all named with the prefix 'test' to stay consistent

def testDatabase() -> None:
    # database loaded successfully
    db = mysql.connector.connect(host="localhost", user="root", passwd="root", database=databaseName)
    assert db.is_connected() == True    # database should be able to connect

    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM job")
    results = mycursor.fetchall()

    assert len(results) >= 1        # There should be something in the database
    assert type(db) == mysql.connector.connection_cext.CMySQLConnection     # database connected correctly

    db.close()
    assert db.is_closed() == True       # database should be able to close if requested
