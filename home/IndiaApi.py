import json
import pandas as pd

url = 'https://www.mohfw.gov.in/'

df = pd.read_html(url)[0]
df.columns = ["Sr.No", "States/UT", "Active", "Recovered", "Deaths", "Confirmed"]
df.drop(df.tail(4).index,inplace=True)
df.drop(df[df['States/UT'] =="Cases being reassigned to states"].index, axis=0, inplace=True)
df.reset_index(inplace=True, drop=True)

# converting string to int
df['Active'] = df['Active'].map(int)
df['Recovered'] = df['Recovered'].map(int)
df['Deaths'] = df['Deaths'].map(int)
df['Confirmed'] = df['Confirmed'].map(int)

# getting index of row having total count
total_index = df[df['States/UT'] == 'Total#'].index.item()

# Used in views.india_tracker to get total count
def get_total_count():
    return [
        df['Active'].iloc[total_index],
        df['Recovered'].iloc[total_index],
        df['Deaths'].iloc[total_index],
        df['Confirmed'].iloc[total_index]
    ]


# Returns dataframe which is used in views.search
def get_data():
    return df


# data for pie chart in india_tracker
def save_pie_json():
    myStates = ["Maharashtra", "Tamil Nadu", "Delhi", "Gujarat", "Rajasthan",
                "Uttar Pradesh", "Madhya Pradesh", "West Bengal", "Karnataka", "Bihar"]

    pie_data = {}
    myStates_confirmed = 0
    myStates_deaths = 0

    for state in myStates:
        confirmed = df[df["States/UT"]
                               == state]["Confirmed"].item()
        deaths = df[df["States/UT"] == state]["Deaths"].item()
        pie_data[state] = {
            "Confirmed": confirmed,
            "Deaths": deaths
        }

        myStates_confirmed += confirmed
        myStates_deaths += deaths

    pie_data["Others"] = {
        "Confirmed": df['Confirmed'].iloc[total_index].item() - myStates_confirmed,
        "Deaths": df['Deaths'].iloc[total_index].item() - myStates_deaths
    }

    out_file = open("home/static/home/india_pie_data.json", "w")
    json.dump(pie_data, out_file)
