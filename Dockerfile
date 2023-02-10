FROM python:3.9-bullseye

RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*s



WORKDIR /app
COPY requirements.txt /app/requirements.txt


RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

RUN apt-get install -y sqlite3 libsqlite3-dev
RUN /usr/bin/sqlite3 /database/scraping_data.db

EXPOSE 8000

CMD ["python", "main.py"]
