# import os
# from django import forms
# from django.core.exceptions import *
#
#
# def validate_file_format(value):
#     for file in value:
#         ext = os.path.splitext(file.name)[1]
#         if ext not in ['.pdf', '.PDF']:
#             raise ValidationError('Unsupported File Format!')
#
#
# class PDFMergeForm(forms.Form):
#     files = forms.FileField(
#         allow_empty_file=False,
#         required=True,
#         widget=forms.FileInput(attrs={'multiple': True}),
#         validators=[validate_file_format]
#     )
#
#     def save(self, *args, **kwargs):
#         input_files = self.files.get_list('{}-files'.format(self.prefix))
#         print(dir(input_files[0]))
#         for file in input_files:
#             print(file)
#         return super().save(*args, **kwargs)
