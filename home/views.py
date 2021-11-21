from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
import folium
import pandas as pd
from pprint import pprint
import requests
import pyowm
from .models import City
from .forms import CityForm

def home(request):
    url = "https://raw.githubusercontent.com/ttran293/cmsc-462/main/rc.csv?token=AK2UTUCNYPQCC7TV6DRLXWDBTW3NI"
    park = pd.read_csv(url)

    park = park[["Latitude", "Longitude", "name", "type", "address"]]


    m = folium.Map(location=[park.Latitude.mean(), park.Longitude.mean()],control_scale=True, zoom_start=11)
    test = folium.Html('<b>Hello world</b>', script=True)

    popup = folium.Popup(test, max_width=2650)

    for index, location_info in park.iterrows():
        text = f"""
        <p><b>Join:</b> {location_info['name']} {location_info['type']}</p>
        <p style="text-align:center;"><b>Address: </b> {location_info['address']}</p>
            """
        folium.Marker([location_info["Latitude"], location_info["Longitude"]], popup=folium.Popup(text, max_width = 400)).add_to(m)

    #tooltip = location_info['type']

    #39.25484512917189, -76.71139655345341

    APIKEY = 'b6e19d92daea6f8d6c533d397f7ef2c5'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + APIKEY

    err_msg = ''
    message = ''
    message_class = ''


    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            # else:
            #     err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            #message = 'City added successfully!'
            message_class = 'is-success'
    else: #set baltimore as default value
        new_city = 'Baltimore'
    form = CityForm()



    cities = City.objects.filter(name=new_city)

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        city_weather = {
            'city' : city.name,
            'city_id': r['id'],
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'id' : r['weather'][0]['id'],
            'APIK' : APIKEY,
        }
        weather_data.append(city_weather)

    m=m._repr_html_() #updated

    return render(request, 'home/home-page.html',
            {'my_map' : m ,
            'weather_data' : weather_data,
            'form' : form,
            'message' : message,
            'message_class' : message_class
            })

def search(request):
    if request.method == "POST":
        results = request.POST['results']
        # shows the search results for the query
        queries = User.objects.filter(username__contains=results)
        return render(request, 'home/search.html', {'results':results, 'queries':queries})
    else:
        # no results found
        return render(request, 'home/search.html')

def support(request):
    return render(request, 'home/support.html')

def about(request):
    return render(request, 'home/about.html')

def sports(request):
    return render(request, 'home/sports.html')
