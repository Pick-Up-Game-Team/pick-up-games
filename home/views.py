from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.middleware.csrf import get_token
import folium
import pandas as pd
import requests
from statistics import mean
from .models import City, Court
from .forms import CityForm
from users.models import Profile

def home(request):
    url = "https://raw.githubusercontent.com/Pick-Up-Game-Team/pick-up-games/main/home/static/db/rc.csv"
    
    courts = Court.objects.all()
    print(courts.exists())
    
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
        # Define marker colors by sport
        SPORT_COLOR = {
            'Basketball': 'orange',
            'Tennis': 'green',
            'Soccer': 'blue',
            'Baseball': 'red',
            'Other': 'darkpurple'
        }
        
        if request.user.is_authenticated:
            user_profile = Profile.objects.get(user=request.user)
        else:
            user_profile = None
        
        # If user is not logged in, do not have a join/leave button
        if not user_profile:
            button = """
                    <div class="d-flex justify-content-center">
                        <input type="submit" class="btn btn-danger" value="Login to join" name="map-login">
                    </div>
                    """
            url = reverse('login')
            method = "GET"
        # Button to leave the court if user is there
        elif user_profile.court == court:
            button = """
                    <div class="d-flex justify-content-center">
                        <input type="submit" class="btn btn-danger" value="Leave" name="leave-court">
                    </div>
                    """
            url = reverse('leave-court', args=(court.pk,))
            method = "POST"
        # Button to join the court if user is not there
        else:
            button = """
                    <div class="d-flex justify-content-center">
                        <input type="submit" class="btn btn-primary" value="Join" name="join-court">
                    </div>
                    """
            url = reverse('join-court', args=(court.pk,))
            method = "POST"
        
        # HTML to embed into marker popup
        text = f"""
        <p>
            <a href="{reverse('court-detail', args=(court.pk,))}" target="_blank">
                <h4>{court.name}</h4>
            </a>
            {court.type_info}
            <br>
        </p>
        <p>
            <b>Main Sport: </b>{court.main_sport}
            <br>
            <b>Address: </b>{court.address}
            <br>
            <b>{court.profile_set.count()} players </b>are currently here
        </p>
        <form action="{url}" method="{method}" target="_parent">
            <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}"/>
            {button}
        </form>
        """
        # Set color of marker based on sport
        icon = folium.Icon(icon='fire', color=SPORT_COLOR[court.main_sport])
        
        folium.Marker([court.latitude, court.longitude], popup=folium.Popup(text, max_width = 400), icon=icon).add_to(m)
    
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

def join_court(request, **kwargs):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        court = Court.objects.get(pk=kwargs['pk'])
        
        court.profile_set.add(user_profile)
        
    return redirect('home-page')

def leave_court(request, **kwargs):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        court = Court.objects.get(pk=kwargs['pk'])
        
        court.profile_set.remove(user_profile)
        
    return redirect('home-page')

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
    """Detailed view of a court"""
    model = Court
    
    def get_context_data(self, **kwargs):
        """Define extra context variables"""
        context = super().get_context_data(**kwargs)
        
        # Default image URLs for each sport
        context['Basketball_img'] = 'https://images.unsplash.com/photo-1616003618448-2914895212ba?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1167&q=80'
        context['Soccer_img'] = 'https://images.unsplash.com/photo-1551958219-acbc608c6377?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
        context['Tennis_img'] = 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
        context['Baseball_img'] = 'https://images.unsplash.com/photo-1530143651579-c7f12d67ae3e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
        context['Other_img'] = 'https://images.unsplash.com/photo-1607962837359-5e7e89f86776?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
        
        # Determine the picture to use based on the main sport of the court
        main_sport = self.object.main_sport
        context['sport_img'] = context[main_sport + '_img']
        
        return context

class CourtListView(ListView):
    model = Court
    