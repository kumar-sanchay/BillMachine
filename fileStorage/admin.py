from django.contrib import admin
from .models import FileStorage


@admin.register(FileStorage)
class FileStorageAdmin(admin.ModelAdmin):
    list_filter = ['created', 'active']
    list_display = ['company', 'to', 'invoice_no']
    search_fields = ['company', 'to', 'invoice_no']