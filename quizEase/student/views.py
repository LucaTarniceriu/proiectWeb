from django.shortcuts import render, redirect


# Create your views here.

def s_home(request):
    return render(request, 'homeS.html')

def joinQuiz(request):
    return render(request, 'joinQuiz.html')

def completedQuizzes(request):
    return render(request, 'completedQuizzes.html')

def s_logout(request):
    return redirect('/quizEase')
