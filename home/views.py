from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
import folium
import pandas as pd
import requests
from statistics import mean
from .models import City, Court
from .forms import CityForm

def home(request):
    url = "https://raw.githubusercontent.com/Pick-Up-Game-Team/pick-up-games/main/home/static/db/rc.csv"
    
    courts = Court.objects.all()
    
    # Load default court data from csv file
    default_courts = pd.read_csv(url)
    default_courts = default_courts[["Latitude", "Longitude", "name", "type", "address"]]
    
    # Create default courts if no courts exist
    if not courts.exists():
        for i, court in default_courts.iterrows():
            new_court = Court(latitude=court['Latitude'],
                              longitude=court['Longitude'],
                              name=court['name'],
                              type_info=court['type'],
                              address=court['address'])
            new_court.save()
    
    courts = list(Court.objects.all())
    
    # Get average latitude of all courts for map start location
    avg_lat = 0
    avg_lat = mean([avg_lat + court.latitude for court in courts])
    
    # Get average longitude of all courts for map start location
    avg_long = 0
    avg_long = mean([avg_long + court.longitude for court in courts])

    # Initialize map
    m = folium.Map(location=[avg_lat, avg_long],control_scale=True, zoom_start=11)

    # Create markers and popups for each court
    for court in courts:
        text = f"""
        <p><a href="#"><h4>{court.name}</h4></a> {court.type_info}</p>
        <p><b>Address: </b> {court.address}</p>
            """
        folium.Marker([court.latitude, court.longitude], popup=folium.Popup(text, max_width = 400)).add_to(m)
    
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
        queries = User.objects.filter(username__contains=results)
        return render(request, 'home/search.html', {'results':results, 'queries':queries})
    else:
        return render(request, 'home/search.html')

def support(request):
    return render(request, 'home/support.html')

def about(request):
    return render(request, 'home/about.html')

def sports(request):
    return render(request, 'home/sports.html')

class CourtDetailView(DetailView):
    model = Court
    
    def get_context_data(self, **kwargs):
        """Define extra context variables"""
        context = super().get_context_data(**kwargs)
        
        # Default image URLs for each sport
        context['basketball_img'] = 'https://images.unsplash.com/photo-1616003618448-2914895212ba?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1167&q=80'
        
        return context
