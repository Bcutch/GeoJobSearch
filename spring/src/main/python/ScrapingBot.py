# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# driver = webdriver.Chrome()

# url = "https://www.google.com/search?q=jobs&ibp=htl;jobs&sa=X&ved=2ahUKEwjdmKzms4iEAxUZFFkFHYiTAcsQudcGKAF6BAgVECk&sxsrf=ACQVn08IIZprvLhsGFSvAMFGPGWZ_OVggQ:1706730829064#htivrt=jobs&fpstate=tldetail&htichips=job_family_1:development%20manager&htischips=job_family_1;development%20manager&htidocid=kJqvmFmCoefvg3SWAAAAAA%3D%3D"

# try:
#     driver.get(url)
#     driver.implicitly_wait(10)
#     page_source = driver.page_source


# finally:
#     # Close the browser window
#     driver.quit()

    
# soup = BeautifulSoup(page_source, 'html.parser')
# i = 1
# print(soup.find_all('div', class_='BjJfJf PUpOsf'))
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https://www.google.com/search?q=jobs+near+me&ibp=htl;jobs&sa=X&ved=2ahUKEwjdmKzms4iEAxUZFFkFHYiTAcsQudcGKAF6BAgVECk&sxsrf=ACQVn08IIZprvLhsGFSvAMFGPGWZ_OVggQ:1706730829064#fpstate=tldetail&htivrt=jobs&htidocid=AlIPyF7QBKHtMqS4AAAAAA%3D%3D"

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
page_source = driver.page_source

# Close the browser window
driver.quit()

# Now you can use BeautifulSoup to parse the page source
soup = BeautifulSoup(page_source, 'html.parser')

# Example: Print the titles of search results
i = 1
for element in (soup.find_all('div', class_='BjJfJf PUpOsf')):
    title = element.text.strip()
    print(i, title)
    i+=1
