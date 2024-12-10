from django.urls import path

from hairSalon.usersApp import views

urlpatterns = (
    path('', views.ProfileDetailView.as_view(), name='profile'),
    path('edit/', views.EditProfileView.as_view(), name='edit'),
    path('delete/', views.DeleteProfileView.as_view(), name='delete'),
)
