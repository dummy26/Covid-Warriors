from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .IndiaApi import save_heat_map, save_pie_chart, save_json, get_data
import json
import pandas

# def homepage(request):
#     return render(request, 'home/homepage.html', {'articles': Article.objects.all()})

# Remove later 
class ArticleListView(ListView):
    model = Article
    template_name = 'home/homepage.html'

# Remove later 
class ArticleDetailView(DetailView):
    model = Article


def live_tracker(request):
    # save_pie_chart()
    save_heat_map()
    data = get_data()
    context = {
        'Active': data[0],
        'Recovered': data[1],
        'Deaths': data[2],
        'Confirmed': data[3],
    }
    return render(request, 'home/live_tracker.html', context)


def search(request):
    # when someone searches and submits form it's a get request
    if request.method == 'GET':
        # gets data from govt site and saves it in data.txt 
        save_json()

        df = pandas.read_json('home/data.txt')
        df.drop(['Sr.No'], axis=1, inplace=True)
        query = request.GET['q'].lower()

        states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadar Nagar Haveli', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
                  'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telengana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal']

        target = ''
        for state in states:
            if state.lower() in query:
                target = state
                break

        andaman_extras = ['andaman', 'andaman and nicobar',
                          'andaman and nicobar island']

        bengal_extras = ['bengal']

        for extra in andaman_extras:
            if extra in query:
                target = 'Andaman and Nicobar Islands'
                break

        for extra in bengal_extras:
            if extra in query:
                target = "West Bengal"
                break

        try:
            Active = df[df['States/UT'] == target]['Active'].iloc[0]
            Recovered = df[df['States/UT'] == target]['Recovered'].iloc[0]
            Deaths = df[df['States/UT'] == target]['Deaths'].iloc[0]
            Confirmed = df[df['States/UT'] == target]['Confirmed'].iloc[0]

        # if target is not in states this exception will be raised
        except IndexError as e:
            # this message will be shown on homepage
            messages.error(request, 'Could not find that')
            return redirect('homepage')
    
        # text_to_speak = 'Active' + str(Active) + \
        #     'Recovered' + str(Recovered) + 'Deaths' + \
        #     str(Deaths) + 'Confirmed' + str(Confirmed)

        recover_percent = round(Recovered/Confirmed*100, 2)
        death_percent = round(Deaths/Confirmed*100, 2)
        
        context = {
            'Active': Active,
            'Recovered': Recovered,
            'Deaths': Deaths,
            'Confirmed': Confirmed,
            'State': target,
            # 'percent': Confirmed/get_data()[3]*100,
            'recover_percent': recover_percent,
            'death_percent': death_percent,
            # 'text_to_speak': text_to_speak,
        }

        return render(request, 'home/search.html', context)


def search_tab(request):
    return render(request, 'home/search_tab.html')
