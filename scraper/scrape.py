import scrapy
import pandas as pd

class TableScraper(scrapy.Spider):
    name = "table_scraper" # name of the spider
    start_urls = [
        'https://www.puertoaltamira.com.mx/engs/0002056/ship-programming-sheet'
    ]
    def parse(self, response):
        data = []
        table = response.css("table.tablaConsulta") # extract the table from the response using CSS selectors
        rows = table.css("tr") # extract the rows from the table
        for row in rows:
            cells = row.css("td") # extract the cells from each row
            row_data = [cell.css("::text").get() for cell in cells] # extract the text from each cell
            data.append(row_data) # add the row data to the list
        self.output = pd.DataFrame(data[1:], columns=data[0]) # create a pandas DataFrame from the data and set the columns
        return self.output
