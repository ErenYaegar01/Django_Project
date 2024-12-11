from django.urls import path
from . import views
from .views import login_view, CustomLogoutView, CustomPasswordResetView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name = 'generator'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login page
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Logout functionality
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('home/', views.home_view, name='home'),  # Home page (this is where users will be redirected after login)
    path('', views.metadata_list, name='metadata_list'),
    path('upload/', views.metadata_upload, name='metadata_upload'),
    path('synthesizer/create/', views.synthesizer_create, name='synthesizer_create'),
    path('synthesizer/', views.synthesizer_list, name='synthesizer_list'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
