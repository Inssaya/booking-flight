from django.urls import path
from . import views


app_name='accounts'
urlpatterns = [
  
    #dont forget tzid url l url l2asli
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile , name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout_view, name='logout'),
    
]