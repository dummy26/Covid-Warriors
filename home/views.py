from django.shortcuts import render, redirect
from .IndiaApi import get_data, get_total_count, save_pie_json
from .statsApi import get_stats
from .utils import add_comas
import pandas

def homepage(request):
    return render(request, 'home/index.html')


def articles(request):
    return render(request, 'home/articles.html')


def india_tracker(request):
    save_pie_json()
    data = get_total_count()
    context = {
        'Active': add_comas(data[0]),
        'Recovered': add_comas(data[1]),
        'Deaths': add_comas(data[2]),
        'Confirmed': add_comas(data[3]),
        'recover_percent': round(data[1]/data[3]*100, 2),
        'death_percent': round(data[2]/data[3]*100, 2),
    }
    return render(request, 'home/india_tracker.html', context)


def search(request):
    # when someone searches and submits form it's a get request
    if request.method == 'GET':
        df = get_data()
        query = request.GET['q'].lower()

        states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadar Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
                  'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal']

        target = ''
        for state in states:
            if state.lower() in query:
                target = state
                break

        if target == '':
            andaman_extras = ['andaman', 'andaman and nicobar',
                              'andaman and nicobar island']

            for extra in andaman_extras:
                if extra in query:
                    target = 'Andaman and Nicobar Islands'
                    break

            if 'bengal' in query:
                target = "West Bengal"

        if target == '':
            jammu_extras = ["jammu", "jammu kashmir", "kashmir"]
            for extra in jammu_extras:
                if extra in query:
                    target = "Jammu and Kashmir"
                    break

            if 'himachal' in query:
                target = "Himachal Pradesh"

        try:
            Active = df[df['States/UT'] == target]['Active'].iloc[0]
            Recovered = df[df['States/UT'] == target]['Recovered'].iloc[0]
            Deaths = df[df['States/UT'] == target]['Deaths'].iloc[0]
            Confirmed = df[df['States/UT'] == target]['Confirmed'].iloc[0]
            recover_percent = round(Recovered/Confirmed*100, 2)
            death_percent = round(Deaths/Confirmed*100, 2)

            total_index = df[df['States/UT'] == 'Total#'].index.item()
            
            Average_active = df['Active'].iloc[total_index].item() / 36
            Average_recovered = df['Recovered'].iloc[total_index].item() / 36
            Average_deaths = df['Deaths'].iloc[total_index].item() / 36
            Average_confirmed = df['Confirmed'].iloc[total_index].item() / 36

            Average_recovered_percent = round(Average_recovered / Average_confirmed * 100, 2)
            Average_deaths_percent =  round(Average_deaths / Average_confirmed * 100, 2)

        # if target is not in states this exception will be raised
        except IndexError as e:
            return redirect('404')

        # tts text
        if Confirmed > Average_confirmed:
            text_to_speak = f"With {Confirmed} total confirmed cases, {target} is in worse condition compared to national average"
            if Active > Average_active:
                text_to_speak += f", also its {Active} active cases are greater than national average."
            elif Active <= Average_active:
                text_to_speak += f", but its {Active} active cases are lesser than national average."

        elif Confirmed <= Average_confirmed:
            text_to_speak = f"With {Confirmed} total confirmed cases, {target} is in better condition compared to national average"
            if Active > Average_active:
                text_to_speak += f", but its {Active} active cases are greater than national average."
            elif Active <= Average_active:
                text_to_speak += f", also its {Active} active cases are lesser than national average."

        context = {
            'State': target,
            'Active': add_comas(Active),
            'Recovered': add_comas(Recovered),
            'Deaths': add_comas(Deaths),
            'Confirmed': add_comas(Confirmed),
            'recover_percent': recover_percent,
            'death_percent': death_percent,
            'text_to_speak': text_to_speak,
            'Average_active': add_comas(int(Average_active)),
            'Average_recovered': add_comas(int(Average_recovered)),
            'Average_deaths': add_comas(int(Average_deaths)),
            'Average_confirmed': add_comas(int(Average_confirmed)),
            'Average_recovered_percent': Average_recovered_percent,
            'Average_deaths_percent' : Average_deaths_percent,
        }

        return render(request, 'home/search_result.html', context)


def search_tab(request):
    return render(request, 'home/search_tab.html')


def page404(request):
    return render(request, 'home/404.html')


def world_tracker(request):
    data = get_stats()
    # If we don't get data from api we request again
    if data == 0:
        return redirect('world_tracker')

    # data from govt site and other api doesn't match so changing it
    india_data = get_total_count()
    data[55] = {'Confirmed': add_comas(india_data[3]),
     'Recovered': add_comas(india_data[1]),
     'Deaths': add_comas(india_data[2])
    }
    
    return render(request, 'home/world_tracker.html', {"data": data})
