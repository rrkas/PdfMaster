from django import forms


class PDFMergeForm(forms.Form):
    files = forms.FileField(
        allow_empty_file=False,
        required=True,
        widget=forms.FileInput(attrs={'multiple': True}),
    )

    def save(self, *args, **kwargs):
        input_files = self.files.get_list()
        print(dir(input_files[0]))
        for file in input_files:
            print(file)
        return super().save(*args, **kwargs)
