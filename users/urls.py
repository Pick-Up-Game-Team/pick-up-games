from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('accManage/', views.manage, name='profile-management'),
    path('ChangePublic/',views.change, name='public-change'),

]