import mysql.connector

# imports will have different paths depending on where the file is run
if __name__ == "__main__":      # if this file is directly run
    import ScrapingBot
else:                           # if this file is indirectly run
    import spring.src.main.python.ScrapingBot as ScrapingBot

db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="testdb")

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

jobDict = ScrapingBot.jobData

for job in jobDict:
    mycursor.execute("""INSERT INTO job (title, url) VALUES ("%s", "%s");""" % (job['title'], job['url']))
    db.commit()

db.close()

# mycursor.execute("SELECT * FROM job")

# for i in mycursor:
#     print(i)
