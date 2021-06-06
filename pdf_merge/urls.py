from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='pdf-merge-home'),
    path('result/', result, name='pdf-merge-result')
]
