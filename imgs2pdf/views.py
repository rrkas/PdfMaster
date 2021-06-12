import io
import os
import uuid
from os.path import join
from typing import List

from django.contrib import messages
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from PIL import Image

upload_root = 'staticfiles'
converted_files = 'converted-files'


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
    return '.' in filename and filename.split('.')[-1].lower() in ['jpg', 'jpeg', 'png', 'gif']


def convert(files: List[TemporaryUploadedFile]) -> str:
    filename = "{}".format(uuid.uuid4().hex)
    imgs = []
    for file in files:
        if allowed_file(file.name):
            if file.name.split('.')[-1] == 'png':
                png = Image.open(file)
                png.load()  # required for png.split()
                background = Image.new("RGB", png.size, (255, 255, 255))
                pngLayers = png.split()
                background.paste(png, mask=pngLayers[3] if len(pngLayers) > 3 else None)  # 3 is the alpha channel
                imgs.append(background)
            else:
                img = Image.open(file)
                img.convert()
                imgs.append(img)
    if len(imgs) > 0:
        if not os.path.exists(join(os.getcwd(), upload_root, converted_files)):
            os.mkdir(join(os.getcwd(), upload_root, converted_files))
        dstFile = join(os.getcwd(), upload_root, converted_files, filename + '.pdf')
        imgs[0].save(dstFile, save_all=True, append_images=imgs[1:])
        return filename
    return 'failure'


def home(request):
    if request.method == 'POST':
        files: List[TemporaryUploadedFile] = request.FILES.getlist('files[]')
        files = list(filter(lambda file: allowed_file(file.name), files))
        if len(files) > 0:
            try:
                res_file_id = convert(files)
                messages.success(request, 'Merge Successful!')
            except BaseException as e:
                print('home-files:', e.args)
                res_file_id = 'error'
                messages.error(request, 'Merge Failed! Something went wrong!', extra_tags='danger')
        else:
            res_file_id = 'failure'
        return redirect('imgs2pdf-result', file_id=res_file_id)
    return render(request, 'imgs2pdf/home.html')


def result(request, file_id):
    filepath = join(os.getcwd(), upload_root, converted_files, file_id + ".pdf")
    success = True
    if not os.path.exists(filepath):
        success = False
    context = {
        'file_id': file_id,
        'success': success,
        'size': pretty_size(os.path.getsize(filepath)) if success else None,
        'path': join(upload_root, converted_files, file_id + ".pdf"),
    }
    return render(request, 'imgs2pdf/result.html', context)


def download(request, file_id):
    file_path = join(os.getcwd(), upload_root, converted_files, file_id + ".pdf")
    # print(file_path)
    if os.path.exists(file_path):
        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)
        os.remove(file_path)
        # print(return_data)
        response = HttpResponse(return_data.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + 'RRKA-PDF-Master-Img2PDF.pdf'
        return response
    raise Http404
