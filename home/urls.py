from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('search/', views.search, name='search'),
    path('support/', views.support, name='support-page'),
    path('about/', views.about, name='about-page'),
    path('sports/', views.sports, name='sports-page'),
    path('courts/', views.CourtListView.as_view(), name='court-list'),
    path('courts/<int:pk>/', views.CourtDetailView.as_view(), name='court-detail'),
    path('courts/<int:pk>/join/', views.join_court, name='join-court'),
    path('courts/<int:pk>/leave/', views.leave_court, name='leave-court')
]
