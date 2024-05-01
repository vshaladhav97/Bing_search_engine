from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', model_form_upload, name='upload'),
    path('success/', upload_success, name='upload_success'),
    path('search/', search_view, name='search_view'),
    path('pdf_viewer/<path:pdf_path>/', pdf_viewer, name='pdf_viewer'),
    path('media/documents/<path:path>/', pdf_serve, name='pdf_serve'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)