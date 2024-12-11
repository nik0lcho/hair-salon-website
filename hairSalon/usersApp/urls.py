from django.urls import path

from hairSalon.usersApp import views

urlpatterns = (
    path('', views.ProfileDetailView.as_view(), name='profile'),
    path('edit/', views.EditProfileView.as_view(), name='edit'),
    path('delete/', views.DeleteProfileView.as_view(), name='delete'),
    path('log-in/', views.LogInProfileView.as_view(), name='log-in'),
    path('register/', views.RegisterProfileView.as_view(), name='register'),
    path('log-out/', views.LogOutProfileView.as_view(), name='log-out')
)
