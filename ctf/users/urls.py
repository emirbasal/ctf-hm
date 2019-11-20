from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.TeamListViewRanking.as_view(), name='home'),
    path('register', views.user_register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile', views.user_profile, name='profile'),
    path('teams', views.TeamsOverview.as_view(), name='teams')

]