from django.http import HttpResponse
from django.shortcuts import render
import folium
import pandas as pd
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
    m=m._repr_html_() #updated
    context = {'my_map': m}
    #39.25484512917189, -76.71139655345341
    return render(request, 'home/home-page.html',context)


def support(request):
    return render(request, 'home/support.html')

def about(request):
    return render(request, 'home/about.html')

def sports(request):
    return render(request, 'home/sports.html')