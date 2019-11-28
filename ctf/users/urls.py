from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.TeamsRankingListView.as_view(), name='home'),
    path('register', views.user_register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile', views.user_profile, name='profile'),
    path('teams', views.TeamsSummaryListAndCreateView.as_view(), name='teams'),
    path('teams/<int:pk>', views.TeamDetail.as_view(), name='team_detail'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user_detail')

]