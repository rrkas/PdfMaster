from django.contrib import messages
from django.shortcuts import *
from .forms import *


def home(request):
    form = PDFMergeForm()
    if request.method == 'POST':
        form = PDFMergeForm(request.POST)
        if form.is_valid():
            files = form.cleaned_data
            try:
                print(files)
            except:
                pass
            messages.success(request, 'Merge Successful!')
            res = 'Success'
        else:
            res = 'Failure'
        return redirect('pdf-merge-result', res=res)
    context = {
        'form': form,
    }
    return render(request, 'pdf_merge/home.html', context)


def result(request):
    res = request.GET
    print(res.res)
    return render(request, 'pdf_merge/result.html', {'result': 'Success'})
