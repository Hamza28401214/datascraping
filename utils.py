import sqlite3
from pathlib import Path
import pandas as pd
pat = str(Path(__file__).parent)


def to_db(df, name):
    con = sqlite3.connect('database//scraping_data.db')
    df.to_sql(con=con, name=name, if_exists='replace')
    con.close()
    return
def read():
    con = sqlite3.connect('database//scraping_data.db')
    res = pd.read_sql_query("SELECT * from data", con)
    res.drop('index', axis=1, inplace=True)
    return res