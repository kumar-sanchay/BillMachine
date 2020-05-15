from django.urls import path
from .views import CreateCompany, CompanyDetail

app_name = 'company'

urlpatterns=[

    path('<int:pk>/<slug:slug>/', CompanyDetail.as_view(), name='detail_company'),
    path('create/', CreateCompany.as_view(), name='create_company'),
]