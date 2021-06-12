import io
from typing import List
from os.path import *
import os
import uuid
import PyPDF2
from django.contrib import messages
from django.shortcuts import *
from django.core.files.uploadedfile import TemporaryUploadedFile

upload_root = 'staticfiles'
merged_files = 'merged-files'


def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ['pdf', 'PDF']


def merge_pdfs(files: List[TemporaryUploadedFile]) -> str:
    filename = "{}".format(uuid.uuid4().hex)
    filepath = join(os.getcwd(), upload_root, merged_files, filename + ".pdf")
    if not os.path.exists(join(os.getcwd(), upload_root, merged_files)):
        os.mkdir(join(os.getcwd(), upload_root, merged_files))
    pdfMerger = PyPDF2.PdfFileMerger()
    files = [file for file in files if file.name.split('.')[-1] in ['pdf', 'PDF']]
    if len(files) == 0:
        return 'failure'
    for file in files:
        # print(file)
        pdfReader = PyPDF2.PdfFileReader(file, 'rb')
        pdfMerger.append(pdfReader)
    pdfMerger.write(filepath)
    return filename


def home(request):
    if request.method == 'POST':
        files: List[TemporaryUploadedFile] = request.FILES.getlist('files[]')
        files = list(filter(lambda file: allowed_file(file.name), files))
        if len(files) > 0:
            try:
                res_file_id = merge_pdfs(files)
                messages.success(request, 'Merge Successful!')
            except BaseException as e:
                # print('home-files:', e.args)
                res_file_id = 'error'
                messages.error(request, 'Merge Failed! Something went wrong!', extra_tags='danger')
        else:
            res_file_id = 'failure'
        return redirect('pdf-merge-result', file_id=res_file_id)
    return render(request, 'pdf_merge/home.html')


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


def result(request, file_id):
    # print('result-file_id:', file_id)
    filepath = join(os.getcwd(), upload_root, merged_files, file_id + ".pdf")
    success = True
    if not os.path.exists(filepath):
        success = False
    context = {
        'file_id': file_id,
        'success': success,
        'size': pretty_size(os.path.getsize(filepath)) if success else None,
        'path': join(upload_root, merged_files, file_id + ".pdf"),
    }
    return render(request, 'pdf_merge/result.html', context)


def download(request, file_id):
    file_path = join(os.getcwd(), upload_root, merged_files, file_id + ".pdf")
    if os.path.exists(file_path):
        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)
        os.remove(file_path)
        response = HttpResponse(return_data.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + 'RRKA-PDF-Master-Merge.pdf'
        return response
    raise Http404
