import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
import json

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
state_data.drop(index=35, axis=0, inplace=True)

# converting string to int 
state_data['Active'] = state_data['Active'].map(int)
state_data['Recovered'] = state_data['Recovered'].map(int)
state_data['Deaths'] = state_data['Deaths'].map(int)
state_data['Confirmed'] = state_data['Confirmed'].map(int)

# getting total
group_size = [state_data['Active'].iloc[35].item(),
              state_data['Recovered'].iloc[35].item(),
              state_data['Deaths'].iloc[35].item(),
              state_data['Confirmed'].iloc[35].item()
              ]


def get_data():
    return group_size


def save_json():
    data_json = state_data.to_json()
    with open('home/data.txt', 'w') as f:
        f.write(data_json)


def save_pie_chart():
    group_labels = ['Active\n' + str(group_size[0]),
                    'Recovered\n' + str(group_size[1]),
                    'Deaths\n' + str(group_size[2]),
                    'Confirmed\n' + str(group_size[3])]
    plt.pie(group_size, labels=group_labels)
    central_circle = plt.Circle((0, 0), 0.5, color='white')
    fig = plt.gcf()
    fig.gca().add_artist(central_circle)
    plt.title('Distribution of cases')
    fig.set_size_inches(5, 3)
    plt.savefig('./media/figures/pie_chart.jpg')


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

    # merge both the dataframes - state_data and map_data
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