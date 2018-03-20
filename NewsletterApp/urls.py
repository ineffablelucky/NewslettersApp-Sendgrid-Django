from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name = 'register'),
    path('send/', views.send_email, name='send_email'),
    path('api/', views.api_request),
    ]
