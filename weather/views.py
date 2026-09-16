import requests
from django.shortcuts import render

def weather_view(request):
    # Get the city name from the search input (defaults to 'London')
    city_name = request.GET.get('city', 'London')
    
    weather_data = None
    error_message = None
    
    # 1. Look up coordinates using Open-Meteo Geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    
    try:
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if 'results' in geo_data and len(geo_data['results']) > 0:
            location = geo_data['results'][0]
            latitude = location['latitude']
            longitude = location['longitude']
            
            # Format display name nicely with country if available
            display_name = f"{location.get('name')}, {location.get('country', '')}".strip(', ')
            
            # 2. Fetch the weather forecast using the retrieved coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            weather_response = requests.get(weather_url)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json().get('current_weather')
            else:
                error_message = "Could not fetch weather data for this location."
        else:
            error_message = f"City '{city_name}' not found. Please try another name."
            display_name = city_name
            
    except requests.RequestException:
        error_message = "Network error while connecting to the weather service."
        display_name = city_name

    context = {
        'weather': weather_data,
        'city': city_name,
        'display_name': display_name if 'display_name' in locals() else city_name,
        'error': error_message,
    }
    return render(request, 'weather.html', context)