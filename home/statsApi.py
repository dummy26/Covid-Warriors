import requests
import json
import pandas as pd
from .utils import add_comas


def get_stats():
    url = 'https://api.covid19api.com/summary'
    response = requests.get(url)
    if response.status_code != 200:
        return 0
    else:
        df = pd.DataFrame.from_dict(response.json().get('Countries'))
        df.drop(["CountryCode", "Slug", "Date"], axis=1, inplace=True)

        countries = ['Afghanistan', 'Angola', 'Albania', 'United Arab Emirates', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 'Bulgaria', 'Bosnia and Herzegovina', 'Belarus', 'Bolivia', 'Brazil', 'Bhutan', 'Botswana', 'Central African Republic', 'Canada', 'Switzerland', 'Chile', 'China', "Côte d'Ivoire", 'Cameroon', 'Colombia', 'Costa Rica', 'Cuba', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominican Republic', 'Algeria', 'Ecuador', 'Egypt', 'Eritrea', 'Spain', 'Ethiopia', 'Finland', 'France', 'Gabon', 'United Kingdom', 'Ghana', 'Guinea', 'Equatorial Guinea', 'Greece', 'Guatemala', 'Guyana', 'Hungary', 'Indonesia', 'India', 'Ireland', 'Iran, Islamic Republic of', 'Iraq', 'Iceland', 'Israel', 'Italy', 'Jordan', 'Japan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 'Cambodia',
                     'Korea (South)', 'Republic of Kosovo', 'Kuwait', 'Lao PDR', 'Liberia', 'Libya', 'Sri Lanka', 'Lithuania', 'Luxembourg', 'Latvia', 'Morocco', 'Moldova', 'Madagascar', 'Mexico', 'Macedonia, Republic of', 'Mali', 'Myanmar', 'Montenegro', 'Mongolia', 'Mozambique', 'Mauritania', 'Malaysia', 'Namibia',  'Niger', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Papua New Guinea', 'Poland', 'Portugal', 'Paraguay', 'Qatar', 'Romania', 'Russian Federation', 'Western Sahara', 'Saudi Arabia', 'Sudan', 'South Sudan', 'Senegal', 'Sierra Leone', 'Somalia', 'Serbia', 'Suriname', 'Slovakia', 'Sweden', 'Swaziland', 'Syrian Arab Republic (Syria)', 'Chad', 'Togo', 'Thailand', 'Tajikistan', 'Tunisia', 'Turkey', 'Taiwan, Republic of China', 'Tanzania, United Republic of', 'Uganda', 'Ukraine', 'Uruguay', 'United States of America', 'Uzbekistan', 'Venezuela (Bolivarian Republic)', 'Viet Nam', 'Yemen', 'South Africa', 'Zambia', 'Zimbabwe', 'Malawi', 'Rwanda', ]

        data = []
        for country in countries:
            data.append({'Confirmed': add_comas(df[df['Country'] == country]['TotalConfirmed'].item()),
                         'Recovered': add_comas(df[df['Country'] == country]['TotalRecovered'].item()),
                         'Deaths': add_comas(df[df['Country'] == country]['TotalDeaths'].item()),
                         })

        # data for charts in world_tracker.html 
        chart_json_data = {
            "USA": {
                "Confirmed": df[df['Country'] == "United States of America"]['TotalConfirmed'].item(),
                "Deaths": df[df['Country'] == "United States of America"]['TotalDeaths'].item()
            },
            "Brazil": {
                "Confirmed": df[df['Country'] == "Brazil"]['TotalConfirmed'].item(),
                "Deaths": df[df['Country'] == "Brazil"]['TotalDeaths'].item()
            },

            "Russia": {"Confirmed": df[df['Country'] == "Russian Federation"]['TotalConfirmed'].item(),
                       "Deaths": df[df['Country'] == "Russian Federation"]['TotalDeaths'].item()
                       },

            "India": {"Confirmed": df[df['Country'] == "India"]['TotalConfirmed'].item(),
                      "Deaths": df[df['Country'] == "India"]['TotalDeaths'].item()
                      },

            "United Kingdom": {"Confirmed": df[df['Country'] == "United Kingdom"]['TotalConfirmed'].item(),
                               "Deaths": df[df['Country'] == "United Kingdom"]['TotalDeaths'].item()
                               },

            "Spain": {"Confirmed": df[df['Country'] == "Spain"]['TotalConfirmed'].item(),
                      "Deaths": df[df['Country'] == "Spain"]['TotalDeaths'].item()
                      },

            "Peru": {"Confirmed": df[df['Country'] == "Peru"]['TotalConfirmed'].item(),
                     "Deaths": df[df['Country'] == "Peru"]['TotalDeaths'].item()
                     },

            "Italy": {"Confirmed": df[df['Country'] == "Italy"]['TotalConfirmed'].item(),
                      "Deaths": df[df['Country'] == "Italy"]['TotalDeaths'].item()
                      },

            "Chile": {"Confirmed": df[df['Country'] == "Chile"]['TotalConfirmed'].item(),
                      "Deaths": df[df['Country'] == "Chile"]['TotalDeaths'].item()
                      },
            
            "Iran": {"Confirmed": df[df['Country'] == "Iran, Islamic Republic of"]['TotalConfirmed'].item(),
                     "Deaths": df[df['Country'] == "Iran, Islamic Republic of"]['TotalDeaths'].item()
                     },

            "Germany": {"Confirmed": df[df['Country'] == "Germany"]['TotalConfirmed'].item(),
                        "Deaths": df[df['Country'] == "Germany"]['TotalDeaths'].item()
                        },

            "Turkey": {"Confirmed": df[df['Country'] == "Turkey"]['TotalConfirmed'].item(),
                       "Deaths": df[df['Country'] == "Turkey"]['TotalDeaths'].item()
                       },
        }

        # sorting from highest confirmed cases to lowest
        chart_json_data = {k: v for k, v in sorted(chart_json_data.items(), key=lambda item: item[1]['Confirmed'], reverse=True)}

        out_file = open("home/static/home/chart_data.json", "w")
        json.dump(chart_json_data, out_file)

        return data
