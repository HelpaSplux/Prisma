from django.urls import path
from landing import views

app_name = 'landing'

urlpatterns = [
    path('', views.redirect, name='redirect'),
    
]