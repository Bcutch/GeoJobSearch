import sys
import os
import mysql.connector

import scraperToData
import filterJob

check = filterJob.filter("title", "Python Developer")

for i in check:
    print(i)
