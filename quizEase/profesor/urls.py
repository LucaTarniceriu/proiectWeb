from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.p_home),
    path('p_home/', views.p_home, name='p_home'),
    path('createQuiz/', views.createQuiz, name='createQuiz'),
    path('addQuestion/<int:questionNumber>/', views.addQuestion, name='addQuestion'),
    path('viewQuizzes/', views.viewQuizzes, name='viewQuizzes'),
    path('p_logout/', views.p_logout, name='p_logout'),

    path('delete_quiz/<int:quiz_id>/', views.deleteQuiz, name='deleteQuiz'),
    path('solvedQuizzes/<str:quiz_id>/', views.solvedQuizzes, name='solvedQuizzes'),
]