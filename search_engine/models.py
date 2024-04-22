from django.db import models

class Document(models.Model):
    pdf_file = models.FileField(upload_to='documents/')
    content = models.TextField(blank=True)  # Field to store PDF text content
    uploaded_at = models.DateTimeField(auto_now_add=True)