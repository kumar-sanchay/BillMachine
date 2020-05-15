from django.urls import path
from .views import BillForm, bill_pdf

app_name = "fileStorage"

urlpatterns = [
    path('create/<int:pk>/<slug:slug>/', BillForm.as_view(), name="create_bill"),
    path('<int:pk>/<slug:slug>/<int:bill_id>/', bill_pdf, name='create_pdf')

]