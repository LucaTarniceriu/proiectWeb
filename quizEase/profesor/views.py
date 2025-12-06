from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

def p_home(request):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {}
        name = request.user.username.split("@")[0].split(".")
        context['nameStr'] = name[1].title() + " " + name[0].title()
        return render(request, 'homeP.html', context)
    else:
        return redirect('error', error_id='permission_err')
def createQuiz(request):
    if request.user.is_authenticated and request.user.isProfesor:
        return render(request, 'createQuiz.html')
    else:
        return redirect('error', error_id='permission_err')


def viewQuizzes(request):
    if request.user.is_authenticated and request.user.isProfesor:
        return render(request, 'viewQuizzes.html')
    else:
        return redirect('error', error_id='permission_err')

def p_logout(request):
    if request.user.is_authenticated and request.user.isProfesor:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='permission_err')


