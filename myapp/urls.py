from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('donations/', views.donations, name='donations'),
    path('contact/', views.contact, name='contact'),
    path('finance/', views.finance, name='finance'),
    path('communityupdates/', views.community_updates, name='community-updates'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('gallery/', views.gallery, name='gallery'),
    path('starter-page/', views.starter_page, name='starter-page'),
    path('vision/', views.vision, name='vision'),
    path('chathanoor/', views.chathanoor, name='chathanoor'),
    path('kollam/', views.kollam, name='kollam'),
    path('kottiyam/', views.kottiyam, name='kottiyam'),
    path('veliyam/', views.veliyam, name='veliyam'),
    path('attingal/', views.attingal, name='attingal'),
    path('trivandrum/', views.trivandrum, name='trivandrum'),
    path('bangalore/', views.bangalore, name='bangalore'),
    path('success/', views.success, name='success'),
    path('registersuccess/', views.register_success, name='register_success'), 
    path('familytree/', views.familytree, name='familytree'),
    path('calendar/', views.calendar, name='calendar'),
   

    
]
