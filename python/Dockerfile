FROM python:3.9

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
WORKDIR /app
=======
WORKDIR /pythonScraper
>>>>>>> 837dca4 (fixed merge conflict)
=======
WORKDIR /app
>>>>>>> c5734c4 (fixed merge conflict)
=======
WORKDIR /pythonScraper
>>>>>>> 6221bf2 (Python container created and script works for linked in, but when I try to run the container in the dev environment it won't work, only works when i run it as a seperate image)

COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "ScrapingBot.py"]