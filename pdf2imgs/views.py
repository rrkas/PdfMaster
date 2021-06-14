import io
import os
import uuid
from os.path import join
from shutil import *
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pdf2image import convert_from_path

upload_root = 'staticfiles'
converted_files = 'zip-files'


def pretty_size(size):
    if size < 1024:
        return str(size) + " b"
    size //= 1024
    if size < 1024:
        return str(size) + " KB"
    size //= 1024
    if size < 1024:
        return str(size) + " MB"
    size //= 1024
    if size < 1024:
        return str(size) + " GB"


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ['pdf', 'PDF']


def convert(file: InMemoryUploadedFile) -> str:
    filename = "{}".format(uuid.uuid4().hex)
    if not os.path.exists(join(os.getcwd(), upload_root, 'temp')):
        os.mkdir(join(os.getcwd(), upload_root, 'temp'))
    filepath = join(os.getcwd(), upload_root, 'temp', filename + '.pdf')
    with open(filepath, 'wb') as dstn:
        for chunk in file.chunks():
            dstn.write(chunk)
    imgs = convert_from_path(filepath)
    print(type(imgs[0]))
    print(dir(imgs[0]))
    return 'failure'
    # if len(imgs) > 0:
    #     if not os.path.exists(join(os.getcwd(), upload_root, converted_files)):
    #         os.mkdir(join(os.getcwd(), upload_root, converted_files))
    #     dstFile = join(os.getcwd(), upload_root, converted_files, filename + '.zip')
    #     for img in imgs:
    #         img
    #     return filename
    # return 'failure'


def home(request):
    if request.method == 'POST':
        print(dir(request.FILES))
        file: InMemoryUploadedFile = request.FILES['file']
        # files = list(filter(lambda file: allowed_file(file.name), files))
        if allowed_file(file.name):
            # try:
            res_file_id = convert(file)
            # messages.success(request, 'Convert Successful!')
            # except BaseException as e:
            # print('home-files:', e.args)
            res_file_id = 'error'
            messages.error(request, 'Conversion Failed! Something went wrong!', extra_tags='danger')
        else:
            res_file_id = 'failure'
        return redirect('pdf2imgs-result', file_id=res_file_id)
    return render(request, 'pdf2imgs/home.html')


def result(request, file_id):
    filepath = join(os.getcwd(), upload_root, converted_files, file_id + ".zip")
    success = True
    if not os.path.exists(filepath):
        success = False
    context = {
        'file_id': file_id,
        'success': success,
        'size': pretty_size(os.path.getsize(filepath)) if success else None,
        'path': join(upload_root, converted_files, file_id + ".zip"),
    }
    return render(request, 'pdf2imgs/result.html', context)


def download(request, file_id):
    file_path = join(os.getcwd(), upload_root, converted_files, file_id + ".zip")
    # print(file_path)
    if os.path.exists(file_path):
        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)
        os.remove(file_path)
        # print(return_data)
        response = HttpResponse(return_data.read(), content_type="application/zip")
        response['Content-Disposition'] = 'inline; filename=' + 'RRKA-PDF-Master-PDF2Img.zip'
        return response
    raise Http404
