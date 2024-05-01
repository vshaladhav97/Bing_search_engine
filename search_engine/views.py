from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DocumentForm, SearchForm
from .models import Document
import pdfplumber
import re
from django.conf import settings
import os
from django_sendfile import sendfile

def normalize_text(text):
    # Regex improvements for more robust pattern matching
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)
    text = text.replace('\u2013', ' ').replace('\u2014', ' ').replace('\u2010', ' ')
    return text

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('pdf_file')  # Get all uploaded files
            for file in files:
                new_doc = Document(pdf_file=file)
                new_doc.save()  # This step saves the file to the media directory
                try:
                    # Now that the file is saved, you can safely open it
                    with pdfplumber.open(new_doc.pdf_file.path) as pdf:
                        content = ' '.join(normalize_text(page.extract_text() or '') for page in pdf.pages)
                    new_doc.content = content
                    new_doc.save()  # Save the extracted content
                except Exception as e:
                    # Handle exceptions or log errors
                    print(f"Failed to process file {file.name}: {str(e)}")
                    continue
            return redirect('search_view')
        else:
            return render(request, 'file_upload/upload_form.html', {'form': form})
    else:
        form = DocumentForm()
        return render(request, 'file_upload/upload_form.html', {'form': form})

    
def upload_success(request):
    return HttpResponse("Upload successful!")

def search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    queries = request.GET.getlist('query')
    if form.is_valid():
        documents = Document.objects.all()  # Assuming Document is your model
        for query in queries:
            # Use re.escape to escape the entire query string to handle special characters
            # Remove word boundaries for phrases
            if " " in query:
                word_pattern = re.compile(re.escape(query), re.IGNORECASE)
            else:
                word_pattern = re.compile(r'\b' + re.escape(query) + r'\b', re.IGNORECASE)
            
            term_results = [{'document': doc, 'count': len(word_pattern.findall(doc.content))} 
                for doc in documents if isinstance(doc.content, str)]   
            results.append({'term': query, 'results': term_results})
    return render(request, 'file_upload/search.html', {'form': form, 'results': results})


def pdf_viewer(request, pdf_path):
    # print(pdf_path)
    pdf_url = os.path.join(settings.MEDIA_URL, pdf_path)
    # print(pdf_url)
    query = request.GET.get('query', '')
    term_counts = {}  # Calculate term counts here, assuming you have a function to do this
    return render(request, 'file_upload/pdf_viewer.html', {'pdf_url': f"/media/{pdf_path}", 'query': query, 'term_counts': term_counts})

def pdf_serve(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    return sendfile(request, file_path)
