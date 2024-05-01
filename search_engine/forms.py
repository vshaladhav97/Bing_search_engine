from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('pdf_file',)  # Only include the PDF file field for user input

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['pdf_file'].widget = forms.FileInput(attrs={'multiple': True})
        self.fields['pdf_file'].required = False  # Optional, if you don't want to make it mandatory
        if self.instance and self.instance.pk:
            self.fields['content'] = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'readonly': True}), required=False)
            

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for a word', widget=forms.TextInput(attrs={'class': 'search-input'}))