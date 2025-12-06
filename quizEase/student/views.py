from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.

def s_home(request):
    if request.user.is_authenticated:
        context = {}
        name = request.user.username.split("@")[0].split(".")
        context['nameStr'] = name[1].title()[:-2] + " " + name[0].title()
        return render(request, 'homeS.html', context)
    else:
        return redirect('error', error_id='no_login')

def joinQuiz(request):
    if request.user.is_authenticated:
        return render(request, 'joinQuiz.html')
    else:
        return redirect('error', error_id='no_login')

def completedQuizzes(request):
    if request.user.is_authenticated:
        return render(request, 'completedQuizzes.html')
    else:
        return redirect('error', error_id='no_login')

def s_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='no_login')
