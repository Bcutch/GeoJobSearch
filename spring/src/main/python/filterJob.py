import mysql.connector

# after import change the setFilter list false to true based on what you want to filter and change the string after to the filter
# (eg. True, "Part time") then pass the list to the filter function

setFilter = [False, "title", False, "location", False, "salary", False, "field", False, "remoteness", False, "job type"]
# setFilter[0] = True is title, setFilter[2] = location, setFilter[4] = True is salary, setFilter[6] = True is field
# setFilter[8] = True is remoteness, setFilter[10] = True is job type

# function to be called to return the list of jobs with filtered jobs
def filter(filterSettings):

    # must be changed to connect to the database you want to use
    db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="testdb")
    mycursor = db.cursor()

    select = """SELECT * FROM job WHERE"""
    retList = []

    # checks if it needs the 'AND' or not
    firstDone = False

    if filterSettings[0]:
        select = select + " title = '" + filterSettings[1] + "'"
        firstDone = True

    if filterSettings[2]:
        if firstDone:
            select = select + " AND "
        else:
            firstDone = True

        select = select + " location = '" + filterSettings[3] + "'"

    if filterSettings[4]:
        if firstDone:
            select = select + " AND "
        else:
            firstDone = True
        select = select + " salary = '" + filterSettings[5] + "'"

    if filterSettings[6]:
        if firstDone:
            select = select + " AND "
        else:
            firstDone = True
        select = select + " field = '" + filterSettings[7] + "'"

    if filterSettings[8]:
        if firstDone:
            select = select + " AND "
        else:
            firstDone = True
        select = select + " is_remote = '" + filterSettings[9] + "'"

    # job type doesn't exist in database yet

    #if filterSettings[10]:
    #    if firstDone:
    #        select = select + " AND "
    #    else:
    #        firstDone = True
    #    select = select + " job_type = " + filterSettings[11]  + "'"
        
    select = select + ";"

    print(select)

    # select statement using created select statement
    mycursor.execute(select)

    for i in mycursor:
        retList.append(i)

    mycursor.close()
    db.close()

    return retList

    