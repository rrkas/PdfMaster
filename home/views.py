from django.shortcuts import render
from django.template import RequestContext
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


def error_404(request, *args, **kwargs):
    return render(request, 'home/404.html', {})


def error_500(request, *args, **kwargs):
    return render(request, 'home/500.html', {})
