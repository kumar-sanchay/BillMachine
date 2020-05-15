from django.urls import path
from .views import AddDefaultData, Settings, AddExpressionsToFields, AddTotalField, CompanyDetailsSetting,\
    AddorDeleteFields, CompanySearchField, ShowDefaultData, DeleteDefaultData, AddSummationField

app_name = 'essentials'

urlpatterns = [
    path('', Settings.as_view(), name='company_settings'),
    path('details/', CompanyDetailsSetting.as_view(), name='company_details_setting'),
    path('default/', AddDefaultData.as_view(), name='add_default'),
    path('show_default/', ShowDefaultData.as_view(), name='show_default'),
    path('expression/', AddExpressionsToFields.as_view(), name='add_expression'),
    path('total/', AddTotalField.as_view(), name='add_total_field'),
    path('fields/', AddorDeleteFields.as_view(), name='add_or_delete_fields'),
    path('search_field/', CompanySearchField.as_view(), name='search_field_company'),
    path('delete_default_data/', DeleteDefaultData.as_view(), name='delete_default_data'),
    path('summation_field/', AddSummationField.as_view(), name='add_summation_field'),
]