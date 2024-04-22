from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DocumentForm
from .models import Document
import pdfplumber
from .forms import SearchForm
from collections import Counter
import re
from django_sendfile import sendfile


def normalize_text(text):
    # Add space between concatenated words where the first ends with a lowercase letter followed by an uppercase letter
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Optional: Add rules for digits and letters if needed (e.g., "Class3A" -> "Class 3A")
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)

    # Handling cases with different types of hyphens that might not be recognized by pdfplumber
    text = text.replace('\u2013', ' ')  # En-dash
    text = text.replace('\u2014', ' ')  # Em-dash
    text = text.replace('\u2010', ' ')  # Hyphen

    # Normalize Unicode characters to their closest ASCII representation, if applicable (optional, requires 'unidecode' package)
    # from unidecode import unidecode
    # text = unidecode(text)

    return text

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_doc = form.save(commit=False)

            # Open the uploaded PDF file and extract text, ensuring spaces between chunks
            with pdfplumber.open(new_doc.pdf_file) as pdf:
                content = []
                for page in pdf.pages:
                    page_text = page.extract_text() or ''
                    normalized_text = normalize_text(page_text)
                    content.append(normalized_text)
                # Join all text chunks with spaces
                new_doc.content = ' '.join(content)

            new_doc.save()
            return redirect('upload_success')
    else:
        form = DocumentForm()
    return render(request, 'file_upload/upload_form.html', {
        'form': form
    })

def upload_success(request):
    return HttpResponse("Upload successful!")

# def search_view(request):
#     form = SearchForm()
#     documents = []

#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             documents = Document.objects.filter(content__icontains=query)

#     return render(request, 'file_upload/search.html', {
#         'form': form,
#         'documents': documents
#     })



def search_view(request):
    form = SearchForm()
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            documents = Document.objects.filter(content__icontains=query)
            # Regex to find whole words, case insensitive
            word_pattern = re.compile(r'\b' + re.escape(query) + r'\b', re.IGNORECASE)

            for document in documents:
                content = document.content
                # Find all matches using the word_pattern
                matches = word_pattern.findall(content)
                count = len(matches)
                results.append({
                    'document': document,
                    'count': count
                })

    return render(request, 'file_upload/search.html', {
        'form': form,
        'results': results,
        'query': request.GET.get('query', '')
    })

def pdf_viewer(request, pdf_path):
    return render(request, 'file_upload/pdf_viewer.html', {
        'pdf_url': f"/media/{pdf_path}",  # Assuming media files are served from /media/
        'query': request.GET.get('query', '')
    })

def pdf_serve(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    return sendfile(request, file_path)