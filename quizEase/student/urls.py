from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('joinQuiz', views.home, name='joinQuiz'),
    path('completedQuizzes', views.home, name='completedQuizzes'),
    path('logout', views.home, name='logout'),
]