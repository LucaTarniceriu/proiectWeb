from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.welcome),
    path('welcome/', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
