import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from .utils import add_comas


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

        countries = ['Afghanistan', 'Angola', 'Albania', 'United Arab Emirates', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bosnia and Herzegovina', 'Belarus', 'Bolivia', 'Brazil', 'Bhutan', 'Botswana', 'Central African Republic', 'Canada', 'Switzerland', 'Chile', 'China', "Côte d'Ivoire", 'Cameroon', 'Colombia', 'Costa Rica', 'Cuba', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark','Dominican Republic', 'Algeria', 'Ecuador', 'Egypt', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'France', 'Gabon', 'United Kingdom', 'Ghana', 'Guinea', 'Equatorial Guinea', 'Greece', 'Guatemala', 'Guyana', 'Hungary', 'Indonesia', 'India', 'Ireland', 'Iran, Islamic Republic of', 'Iraq', 'Iceland', 'Israel', 'Italy', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Cambodia', 'Korea (South)', 'Republic of Kosovo', 'Kuwait', 'Lao PDR', 'Liberia', 'Libya', 'Sri Lanka', 'Lithuania', 'Luxembourg', 'Latvia', 'Morocco', 'Moldova', 'Madagascar', 'Mexico', 'Macedonia, Republic of', 'Mali', 'Myanmar', 'Montenegro', 'Mongolia', 'Mozambique', 'Mauritania', 'Malaysia', 'Namibia',  'Niger', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Papua New Guinea', 'Poland', 'Portugal', 'Paraguay', 'Qatar', 'Romania', 'Russian Federation', 'Western Sahara', 'Saudi Arabia', 'Sudan', 'South Sudan', 'Senegal', 'Sierra Leone', 'Somalia', 'Serbia', 'Suriname', 'Slovakia', 'Sweden', 'Swaziland', 'Syrian Arab Republic (Syria)', 'Chad', 'Togo', 'Thailand', 'Tajikistan', 'Tunisia', 'Turkey', 'Taiwan, Republic of China', 'Tanzania, United Republic of', 'Uganda', 'Ukraine', 'Uruguay', 'United States of America', 'Uzbekistan', 'Venezuela (Bolivarian Republic)', 'Viet Nam', 'Yemen', 'South Africa', 'Zambia', 'Zimbabwe']

        data = []
        for country in countries:
            data.append({'Confirmed': add_comas(df[df['Country'] == country]['TotalConfirmed'].item()),
            'Recovered': add_comas(df[df['Country'] == country]['TotalRecovered'].item()),
            'Deaths': add_comas(df[df['Country'] == country]['TotalDeaths'].item()),
            })
            # print(country, data[countries.index(country)])

        return data