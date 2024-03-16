FROM python:3.9

WORKDIR /python

COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y cron

COPY . .

CMD ["bash", "setup-cron.sh"]

