from django.shortcuts import render
from .models import *


def home(request):
    context = {
        'menu_items': [
            MenuItem(name='Merge PDFs', img_url='home/item_logos/pdf_merge.png', target_url='pdf-merge-home'),
        ],
    }
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')
