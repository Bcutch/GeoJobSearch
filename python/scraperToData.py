import mysql.connector
import ScrapingBot

# I can't get the local imports to work when running the file directly
# this works but if there is a better way to do this then please change.
# - Jacob
# if __name__ == "__main__":      # imports when running file
#     import ScrapingBot          
# else:                           # imports when another file runs this
#     from . import ScrapingBot


# Updated database connection details
db = mysql.connector.connect(
    host="mysql",  # Updated to the new host
    user="root",  # DB_USER
    passwd="pwd",  # DB_PASSWORD
    database="template_db"  # DB_DATABASE
)


mycursor = db.cursor()

mycursor.execute("DROP TABLE job")

mycursor.execute("""CREATE TABLE IF NOT EXISTS job (
    id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    description TEXT,
    url VARCHAR(2000) NOT NULL,
    salary INT,
    field VARCHAR(255),
    is_remote BOOLEAN NOT NULL DEFAULT FALSE,
    latitude DECIMAL(11,8),
    longitude DECIMAL(11,8)
);""")

jobDict = ScrapingBot.tempData

for job in jobDict:
    print(job)
    mycursor.execute("""INSERT INTO job (title, url) VALUES ("%s", "%s");""" % (job['title'], job['url']))
    db.commit()

db.close()

# mycursor.execute("SELECT * FROM job")

# for i in mycursor:
#     print(i)
