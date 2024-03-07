<<<<<<< HEAD:spring/src/test/python/filterJobTest.py
import filterJob

settings = filterJob.setFilter
settings[0] = True
settings[1] = "Python Developer"

check = filterJob.filter(settings)

for i in check:
    print(i)

print("\nThen\n")

settings[8] = True
settings[9] = "0"

check = filterJob.filter(settings)

for i in check:
    print(i)

print("\nThen\n")

settings[9] = "1"

check = filterJob.filter(settings)

for i in check:
    print(i)
=======
import sys
import os
import mysql.connector

import scraperToData
import filterJob

check = filterJob.filter("title", "Python Developer")

for i in check:
    print(i)
>>>>>>> 0d6282e63ed25a1cceb909ba7cd2fb73e28096c8:python/filterJobTest.py
