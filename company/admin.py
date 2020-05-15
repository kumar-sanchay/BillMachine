from django.contrib import admin
from .models import Company, BillTitle


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['created', 'active']
    list_display = ['company_name', 'company_email']
    search_fields = ['company_name', 'company_email', 'pincode']


@admin.register(BillTitle)
class BillTitleAdmin(admin.ModelAdmin):
    list_display = ['company']
    list_filter = ['created', 'active']

