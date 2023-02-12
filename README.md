## Introduction
This project is a web scraping api writen in python , compares data and answers to the following questions:
- When a new vessel schedule appears
- When an existing vessel schedule is updated (e.g. vessel has delayed ETA)
- The cargo onboard the vessel
- The export/import movement of the vessel

## Installation

It requires python 3.7+ to run.

Install the dependencies and devDependencies and start the server.

```sh
> python -m venv env
> cd env/scripts
> activate
> cd ../..
> pip install -r requirements.txt
```

## Run

Run ..
```sh
> python -m uvicorn main:app
```
Verify the deployment by navigating to your server address in
your preferred browser.
```sh
127.0.0.1:8000
```
- 127.0.0.1:8000/scrape  : will run the scraping function and save data to a database.
- 127.0.0.1:8000/NewVessel : will show new vessels if new vessel schedule appears.
- 127.0.0.1:8000/vesselUpdates : will show existing vessel schedule when it is updated.

## Docker

It is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.
- Build the image
```sh
>  docker build -t tag1 .
```
- Run the image in a container
```sh
>  docker run -d -p 8000:8000 -v /home/dbfolder/:/db tag1
```

Verify the deployment by navigating to your server address in
your preferred browser.
```sh
127.0.0.1:8000
```
