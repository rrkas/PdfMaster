from django.shortcuts import render
from .models import *


def home(request):
    user_agent = request.user_agent
    context = {
        'menu_items': [
            MenuItem(name='Merge PDFs', img_url='home/item_logos/pdf_merge.png', target_url='pdf-merge-home'),
            MenuItem(name='Images to PDF', img_url='home/item_logos/imgs2pdf.png', target_url='imgs2pdf-home'),
            MenuItem(name='PDF to Image', img_url='home/item_logos/pdf2imgs.png', target_url='pdf2imgs-home'),
        ],
        'small': (user_agent.is_mobile or user_agent.is_tablet),
    }
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def error_404(request, *args, **kwargs):
    return render(request, 'home/404.html', {})


def error_500(request, *args, **kwargs):
    return render(request, 'home/500.html', {})
