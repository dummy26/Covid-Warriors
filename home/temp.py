import concurrent.futures
import time
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
import json

start = time.perf_counter()

if __name__ == "__main__":
    url = 'https://www.mohfw.gov.in/'
    web_content = requests.get(url).content
    soup = BeautifulSoup(web_content, "html.parser")

    # remove any newlines and extra spaces from left and right

    def extract_contents(row):
        return [x.text.replace('\n', '') for x in row]

    stats = []
    # find all table rows and data cells within
    all_rows = soup.find_all('tr')

    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        stats = [executor.map(extract_contents, row.find_all('td')) for row in all_rows]

    finish = time.perf_counter()
    print('Time: ', round(finish-start, 2))
