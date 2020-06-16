import json
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.mohfw.gov.in/'
web_content = requests.get(url).content
soup = BeautifulSoup(web_content, "html.parser")

# remove any newlines and extra spaces from left and right


def extract_contents(row): return [x.text.replace('\n', '') for x in row]


stats = []
# find all table rows and data cells
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
state_data.drop(state_data[state_data['States/UT'] ==
                           "Cases being reassigned to states"].index, axis=0, inplace=True)
state_data.reset_index(inplace=True, drop=True)

# converting string to int
try:
    state_data['Active'] = state_data['Active'].map(int)
    state_data['Recovered'] = state_data['Recovered'].map(int)
    state_data['Deaths'] = state_data['Deaths'].map(int)
    state_data['Confirmed'] = state_data['Confirmed'].map(int)
except Exception as e:
    print("Error in mapping to int")

# getting index of row having total count
total_index = state_data[state_data['States/UT'] == 'Total#'].index.item()

state_data['States/UT'].replace('Daman & Diu', 'Daman and Diu', inplace=True)

# data for pie chart in india_tracker
def save_pie_json():
    myStates = ["Maharashtra", "Tamil Nadu", "Delhi", "Gujarat", "Rajasthan",
                "Uttar Pradesh", "Madhya Pradesh", "West Bengal", "Karnataka", "Bihar"]

    pie_data = {}
    myStates_confirmed = 0
    myStates_deaths = 0

    for state in myStates:
        confirmed = state_data[state_data["States/UT"]
                               == state]["Confirmed"].item()
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
def get_total_count():
    return [
        state_data['Active'].iloc[total_index].item(),
        state_data['Recovered'].iloc[total_index].item(),
        state_data['Deaths'].iloc[total_index].item(),
        state_data['Confirmed'].iloc[total_index].item()
    ]

# Returns dataframe which is used in views.search
def get_data():
    return state_data