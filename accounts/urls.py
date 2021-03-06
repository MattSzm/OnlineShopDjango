from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='registration/logged.html'
    ), name='logout'),
    path('register/', accounts_views.register, name='register' ),
    path('profile/dashboard', accounts_views.userDashboard.as_view(),
         name='dashboard'),
    ]