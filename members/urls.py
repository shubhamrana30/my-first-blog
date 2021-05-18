from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.members_register, name='members_register'),
    path('', views.test, name='test'),
    path('login/adm/', views.test, name='test'),
    path('logout/adm/', views.test, name='test'),
    
]