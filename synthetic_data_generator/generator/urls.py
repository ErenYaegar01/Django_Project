from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import  home,user_login, generate_metadata, upload_file, logout_view, custom_logout
app_name = 'generator' 
urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('generate-metadata/', generate_metadata, name='generate_metadata'),
    path('upload/', upload_file, name='upload_file'),
    path('logout/', logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
      path('logout/', custom_logout, name='logout'),
]
