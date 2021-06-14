from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='pdf2imgs-home'),
    path('result/<file_id>', home, name='pdf2imgs-result'),
    path('download/<file_id>', home, name='pdf2imgs-download'),
]