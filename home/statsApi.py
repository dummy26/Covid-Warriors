import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def get_stats():
    url = 'https://api.covid19api.com/summary'
    response = requests.get(url)
    if response.status_code != 200:
        return 0
    else:
        x = response.json()
        t = x.get('Countries')

        df = pd.DataFrame.from_dict(t)
        df.drop(["CountryCode", "Slug", "Date"], axis=1, inplace=True)

        india_confirmed = df[df['Country'] == 'India']['TotalConfirmed'].item()
        china_confirmed = df[df['Country'] == 'China']['TotalConfirmed'].item()
        usa_confirmed = df[df['Country'] ==
                           'United States of America']['TotalConfirmed'].item()
        confirmed = [india_confirmed, china_confirmed, usa_confirmed]

        india_recovered = df[df['Country'] == 'India']['TotalRecovered'].item()
        china_recovered = df[df['Country'] == 'China']['TotalRecovered'].item()
        usa_recovered = df[df['Country'] ==
                           'United States of America']['TotalRecovered'].item()
        recovered = [india_recovered, china_recovered, usa_recovered]

        india_deaths = df[df['Country'] == 'India']['TotalDeaths'].item()
        china_deaths = df[df['Country'] == 'China']['TotalDeaths'].item()
        usa_deaths = df[df['Country'] ==
                        'United States of America']['TotalDeaths'].item()
        deaths = [india_deaths, china_deaths, usa_deaths]
        india_recovered_percent = round(
            india_recovered / india_confirmed * 100, 2)
        china_recovered_percent = round(
            china_recovered / china_confirmed * 100, 2)
        usa_recovered_percent = round(usa_recovered / usa_confirmed * 100)
        recovered_percent = [india_recovered_percent,
                             china_recovered_percent, usa_recovered_percent]

        india_deaths_percent = round(india_deaths / india_confirmed * 100, 2)
        china_deaths_percent = round(china_deaths / china_confirmed * 100, 2)
        usa_deaths_percent = round(usa_deaths / usa_confirmed * 100, 2)
        deaths_percent = [india_deaths_percent,
                          china_deaths_percent, usa_deaths_percent]
        return {'india_confirmed': india_confirmed, 'china_confirmed': china_confirmed, 'usa_confirmed': usa_confirmed,
                'india_recovered': india_recovered, 'china_recovered': china_recovered, 'usa_recovered': usa_recovered,
                'india_deaths': india_deaths, 'china_deaths': china_deaths, 'usa_deaths': usa_deaths,
                'india_recovered_percent': india_recovered_percent, 'china_recovered_percent': china_recovered_percent, 'usa_recovered_percent': usa_recovered_percent,
                'india_deaths_percent': india_deaths_percent, 'china_deaths_percent': china_deaths_percent, 'usa_deaths_percent': usa_deaths_percent,
                }
