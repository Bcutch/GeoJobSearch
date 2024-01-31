import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https://ca.indeed.com/jobs?q=python&l=Guelph%2C+ON&vjk=1f3e66712fb1ef37"

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
page_source = driver.page_source

# Close the browser window
driver.quit()

# Now you can use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')
for element in soup.find_all('h2', class_='jobTitle'):
    anchorTag = element.find('a')
    if anchorTag:
        link = anchorTag.get('href')
        print(link)
    print(element.text)



