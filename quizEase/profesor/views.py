from django.shortcuts import render, redirect


# Create your views here.

def p_home(request):
    return render(request, 'homeP.html')
def createQuiz(request):
    return render(request, 'createQuiz.html')
def viewQuizzes(request):
    return render(request, 'viewQuizzes.html')
def p_logout(request):
    return redirect('/quizEase')

