from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('accManage/', views.manage, name='profile-management'),
    path('ChangePublic/',views.change, name='public-change'),
    path('<username>/', views.profile_detail, name='profile_detail'),
    path('my-invites/', views.invites_received_view, name='my-invites-view'),
    path('all-profiles/', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('to-invite/', views.invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_from_friends, name='remove-friend'),

]