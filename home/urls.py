from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home-home'),
    path('about/', about, name='home-about'),
]
