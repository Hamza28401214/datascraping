from fastapi import FastAPI
import sys
import requests
from scrapy.http import HtmlResponse
from scraper.scrape import TableScraper
import logging
import uvicorn
from utils import *

logging.basicConfig(filename='logs/record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = FastAPI()

# Create an instance of the TableScraper class
scraper = TableScraper()

# Get the first URL in the start_urls attribute
url = scraper.start_urls[0]

# Make a GET request to the URL using the requests library
response = requests.get(url)

# Create a HtmlResponse object from the response obtained from the requests library
selector = HtmlResponse(url=response.url, body=response.content, encoding='utf-8')

@app.get("/")
async def home():
    return "Hello"

@app.get("/scrape")
async def get_data():
    global data
    # In this code, the purpose of removing the "twisted.internet.reactor" module from the "sys.modules" dictionary is to allow it to be reloaded as if it was imported for the first time
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
    # Call the parse method of the TableScraper class and pass the HtmlResponse object as an argument
    data = scraper.parse(selector)
    data.columns = data.columns.str.strip()
    to_db(data, 'data')
    cols = ['Code', 'Arrival Date', 'Ship', 'Type', 'Origin Port', 'Destination Port', 'Operations', 'Unberthing Date']
    return data[cols].to_dict()
@app.get("/NewVessel")
async def read_data():
    old_data = read()

    # Get the list of vessel codes in the new data
    new_codes = set(data["Code"])

    # Get the list of vessel codes in the old data
    old_codes = set(old_data["Code"])

    # Determine if there are any new vessel codes
    new_vessel_codes = new_codes - old_codes

    # Compare the two sets of data to see if there are any updates
    # updates = data[~data.isin(old_data)].dropna(how="all")
    # If there are any new vessel codes, send a notification to the market analyst
    if new_vessel_codes:
        updated_vessels = data[data["Code"].isin(new_vessel_codes)]
        return updated_vessels.to_dict()
    else:
        return {"There are no updates"}


@app.get("/vesselUpdates")
async def see_updates():
    old_data = read()
    # Get the codes for the vessels that exist in both the old and new data
    existing_vessel_codes = set(old_data["Code"]) & set(data["Code"])

    # Initialize an empty list to store the updated vessels
    updated_vessels = []

    # Loop over the existing vessel codes
    for code in existing_vessel_codes:
        # Get the old and new data for the current vessel code
        old_vessel = old_data[old_data["Code"] == code]
        new_vessel = data[data["Code"] == code]

        # Initialize a flag to indicate if the vessel data has been updated
        is_updated = False

        # Loop over the columns of the old and new vessel data
        for col in old_vessel.columns:
            # Compare the values in the current column of the old and new vessel data
            if old_vessel[col].values != new_vessel[col].values:
                # If the values are different, set the update flag to True
                is_updated = True
                break

        # If the vessel data has been updated
        if is_updated:
            # Add the updated vessel data to the list of updated vessels
            updated_vessels.append({
                "Code": code,
                "Old data": old_vessel.to_dict(orient='records'),
                "New data": new_vessel.to_dict(orient='records')
            })

    # Return the list of updated vessels
    return updated_vessels
