from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('search/', views.search, name='search'),
    path('support/', views.support, name='support-page'),
    path('about/', views.about, name='about-page'),
    path('sports/', views.sports, name='sports-page'),
    path('courts/<int:pk>/', views.sports, name='court-detail')
]
