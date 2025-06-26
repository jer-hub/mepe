from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    path('<int:chapa>/', views.particulars, name='particulars'),
]