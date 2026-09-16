from django.urls import path
from .views import weather_view

urlpatterns = [
    path('', weather_view, name='weather'),        # Makes http://127.0.0.1:8000/ work
    path('weather/', weather_view, name='weather_alt'), # Keeps /weather/ working too
]