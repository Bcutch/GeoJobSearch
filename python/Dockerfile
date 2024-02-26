FROM python:3.9

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> fc1483f (.fixed merge conflict)
=======
>>>>>>> c4dac48 (fixed merge conflict)
WORKDIR /app
=======
WORKDIR /pythonScraper
>>>>>>> 837dca4 (fixed merge conflict)
<<<<<<< HEAD
<<<<<<< HEAD
=======
WORKDIR /app
>>>>>>> c5734c4 (fixed merge conflict)
=======
WORKDIR /pythonScraper
>>>>>>> 6221bf2 (Python container created and script works for linked in, but when I try to run the container in the dev environment it won't work, only works when i run it as a seperate image)
=======
WORKDIR /app
>>>>>>> f63602f (Created Selenium service so that python container can connect to the standalone chrome browser through the docker environmnet, and got python to scrape linkedIn on the environment)
=======
>>>>>>> fc1483f (.fixed merge conflict)
=======
=======
WORKDIR /app
>>>>>>> c5734c4 (fixed merge conflict)
>>>>>>> c4dac48 (fixed merge conflict)

COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "ScrapingBot.py"]