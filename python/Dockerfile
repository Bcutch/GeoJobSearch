FROM python:3.9

WORKDIR /python

COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python main.py

