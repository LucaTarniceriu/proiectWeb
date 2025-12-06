from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome),
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('login_user/', views.login_user, name='login_user'),
    path('error/<str:error_id>/', views.error, name='error'),
]
