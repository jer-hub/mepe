from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    path('checkaccount/', views.checkaccount, name='checkaccount'),
    path('particulars/<int:chapa>/', views.particulars, name='particulars'),
]