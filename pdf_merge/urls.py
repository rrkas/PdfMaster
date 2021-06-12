from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='pdf-merge-home'),
    path('result/<file_id>', result, name='pdf-merge-result'),
    path('download/<file_id>', download, name='pdf-merge-download')
]
