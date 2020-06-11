import json
import geopandas as gpd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
# To solve RuntimeError
matplotlib.use('Agg')

url = 'https://www.mohfw.gov.in/'
web_content = requests.get(url).content
soup = BeautifulSoup(web_content, "html.parser")

# remove any newlines and extra spaces from left and right


def extract_contents(row): return [x.text.replace('\n', '') for x in row]


stats = []
# find all table rows and data cells within
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    # the data we want has 6 columns
    if len(stat) == 6:
        stats.append(stat)

# convert the data into a pandas dataframe
new_cols = ["Sr.No", "States/UT", "Active", "Recovered", "Deaths", "Confirmed"]
state_data = pd.DataFrame(data=stats, columns=new_cols)

# Cases being reassigned to states row causes problem when mapping to int because of missing value
state_data.drop(state_data[state_data['States/UT'] == "Cases being reassigned to states"].index, axis=0, inplace=True)
state_data.reset_index(inplace=True, drop=True)

# converting string to int
try:
    state_data['Active'] = state_data['Active'].map(int)
    state_data['Recovered'] = state_data['Recovered'].map(int)
    state_data['Deaths'] = state_data['Deaths'].map(int)
    state_data['Confirmed'] = state_data['Confirmed'].map(int)
except Exception as e:
    print("Error in mapping to int")

# getting total of each category
total_index = state_data[state_data['States/UT'] == 'Total#'].index.item()

state_data['States/UT'].replace('Daman & Diu', 'Daman and Diu', inplace=True)

# data for pie chart in india_tracker
def save_json():
    # pie_data = state_data.to_json()
    myStates = ["Maharashtra", "Tamil Nadu", "Delhi", "Gujarat", "Rajasthan",
              "Uttar Pradesh", "Madhya Pradesh", "West Bengal", "Karnataka", "Bihar"]
    pie_data = {}
    myStates_confirmed = 0
    myStates_deaths = 0
    for state in myStates:
        confirmed = state_data[state_data["States/UT"] == state]["Confirmed"].item()
        deaths = state_data[state_data["States/UT"] == state]["Deaths"].item()
        pie_data[state] = {
            "Confirmed": confirmed,
            "Deaths": deaths
        }
        myStates_confirmed += confirmed
        myStates_deaths += deaths


    pie_data["Others"] = {
        "Confirmed": state_data['Confirmed'].iloc[total_index].item() - myStates_confirmed,
        "Deaths": state_data['Deaths'].iloc[total_index].item() - myStates_deaths
    }

    out_file = open("home/static/home/india_pie_data.json", "w")
    json.dump(pie_data, out_file)


# Used in views.india_tracker to get total count
def get_data():
    group_size = [state_data['Active'].iloc[total_index].item(),
              state_data['Recovered'].iloc[total_index].item(),
              state_data['Deaths'].iloc[total_index].item(),
              state_data['Confirmed'].iloc[total_index].item()
              ]
    return group_size


# Saves data.txt which is used in views.search
def save_data():
    data_json = state_data.to_json()
    with open('home/data.txt', 'w') as f:
        f.write(data_json)


def save_heat_map():
    map_data = gpd.read_file('./media/india_map/Indian_States.shp')
    map_data.rename(columns={'st_nm': 'States/UT'}, inplace=True)

    # correct the name of states in the map dataframe
    map_data['States/UT'] = map_data['States/UT'].str.replace('&', 'and')
    map_data['States/UT'].replace('Arunanchal Pradesh',
                                  'Arunachal Pradesh', inplace=True)
    map_data['States/UT'].replace('Dadara and Nagar Havelli',
                                  'Dadar Nagar Haveli', inplace=True)
    map_data['States/UT'].replace('Andaman and Nicobar Island',
                                  'Andaman and Nicobar Islands', inplace=True)
    map_data['States/UT'].replace('NCT of Delhi', 'Delhi', inplace=True)
    map_data['States/UT'].replace('Telangana', 'Telengana', inplace=True)

    # merge state_data and map_data
    merged_data = pd.merge(map_data, state_data, how='left', on='States/UT')
    merged_data.fillna(0, inplace=True)
    merged_data.drop('Sr.No', axis=1, inplace=True)

    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(20, 12))
    ax.axis('off')
    ax.set_title('Covid-19 Statewise Data')
    merged_data.plot(column='Confirmed', cmap='tab10',
                     linewidth=0.8, ax=ax, edgecolor='0.6', legend=True)
    plt.gcf().set_size_inches(7, 6)
    plt.savefig('./media/figures/heat_map.jpg')
