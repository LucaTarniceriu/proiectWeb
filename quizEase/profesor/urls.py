from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('createQuiz', views.home, name='createQuiz'),
    path('viewQuizzes', views.home, name='viewQuizzes'),
    path('logout', views.home, name='logout'),
]