from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.s_home),
    path('s_home/', views.s_home, name='s_home'),
    path('joinQuiz/', views.joinQuiz, name='joinQuiz'),
    path('completedQuizzes/', views.completedQuizzes, name='completedQuizzes'),
    path('s_logout/', views.s_logout, name='s_logout'),
]