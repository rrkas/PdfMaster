from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='imgs2pdf-home'),
    path('result/<file_id>', result, name='imgs2pdf-result'),
    path('download/<file_id>', download, name='imgs2pdf-download'),
]
