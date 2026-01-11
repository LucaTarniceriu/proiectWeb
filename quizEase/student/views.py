from asyncio import current_task
from contextlib import nullcontext
from logging import NullHandler

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import Quiz, Question, Submits

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

def activeQuiz(request):
    if request.user.is_authenticated:
        context = {}
        # quiz = Quiz.objects.get(id=request.user.activeQuiz)


        if request.method == "POST":
            print(request.POST['source'])
            if request.POST["source"] == "join":
                formId = request.POST["quiz_code"]
                finishedQuizzes = request.user.finishedQuizzes.split(";")
                if formId in finishedQuizzes:
                    return redirect('error', error_id='already_responded')
                request.user.activeQuiz = formId
                quiz = Quiz.objects.get(id=formId)
                request.user.activeQuestion = Question.objects.get(quiz=quiz, questionNumber=0).id
                request.user.save()
                allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                if allowReturn == "allow_return":
                    context["allowReturn"] = True
                else:
                    context["allowReturn"] = False
                context["title"] = quiz.title
                context["instructions"] = quiz.instructions
                context["questionNo"] = 0
                context["isFirstQuestion"] = True
                context["button"] = "Start quiz"
            if request.POST["source"] == "nextQ":
                if request.POST["submit"] == "Previous Question":
                    print("previous")
                    currentQ = Question.objects.get(id=request.user.activeQuestion).questionNumber
                    allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                    if allowReturn == "allow_return":
                        context["allowReturn"] = True
                    else:
                        context["allowReturn"] = False
                    # request.POST[""]
                    if currentQ > 2:
                        currentQ -= 1
                        request.user.activeQuestion = Question.objects.get(quiz=Quiz.objects.get(id=request.user.activeQuiz), questionNumber=currentQ).id
                        request.user.save()
                        context["questionNo"] = Question.objects.get(id=request.user.activeQuestion).questionNumber
                        context["button"] = "Next question"
                        context["isFirstQuestion"] = False
                    elif currentQ == 2:
                        currentQ -= 1
                        request.user.activeQuestion = Question.objects.get(quiz=Quiz.objects.get(id=request.user.activeQuiz), questionNumber=currentQ).id
                        request.user.save()
                        context["isFirstQuestion"] = True
                        context["questionNo"] = 1
                        context["button"] = "Next question"
                    quiz = Quiz.objects.get(id=request.user.activeQuiz)
                    context["title"] = quiz.title
                    context["question"] = Question.objects.get(id=request.user.activeQuestion).text
                    context["answer"] = Question.objects.get(id=request.user.activeQuestion).answers.split(';')
                    studentAnswers = ""
                    for answer in request.POST.getlist("answers"):
                        studentAnswers += (answer + ";")
                        correctAnswers = Question.objects.get(id=request.user.activeQuestion).correctAnswer
                        score = 0
                        if correctAnswers == studentAnswers:
                            score = Question.objects.get(id=request.user.activeQuestion).points

                    Submits.objects.update_or_create(student=request.user.email, question_id=Question.objects.get(id=request.user.activeQuestion).id, answers=studentAnswers, quiz_id=quiz.id, points=score)

                elif request.POST["submit"] == "Next question" or request.POST["submit"] == "Finish quiz" or request.POST["submit"] == "Start quiz":
                    print("next")
                    quiz = Quiz.objects.get(id=request.user.activeQuiz)
                    context["title"] = quiz.title
                    context['questionNo'] = Question.objects.get(id=request.user.activeQuestion).questionNumber
                    allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                    if allowReturn == "allow_return":
                        context["allowReturn"] = True
                    else:
                        context["allowReturn"] = False
                    if int(context["questionNo"]) > 0:
                        studentAnswers = ""
                        for answer in request.POST.getlist("answers"):
                            studentAnswers += (answer + ";")
                            correctAnswers = Question.objects.get(id=request.user.activeQuestion).correctAnswer
                            score = 0
                            if correctAnswers == studentAnswers:
                                score = Question.objects.get(id=request.user.activeQuestion).points

                        Submits.objects.update_or_create(student=request.user.email, question_id=Question.objects.get(id=request.user.activeQuestion).id, answers=studentAnswers, quiz_id=quiz.id, points=score)

                    context["isFirstQuestion"] = False
                    currentQuestion = Question.objects.get(id=request.user.activeQuestion)

                    if currentQuestion.questionNumber < Quiz.objects.get(id=request.user.activeQuiz).nrOfQuestions - 1:
                        request.user.activeQuestion = Question.objects.get(quiz=Quiz.objects.get(id=request.user.activeQuiz), questionNumber=int(currentQuestion.questionNumber) + 1).id
                        request.user.save()
                        context["questionNo"] = Question.objects.get(id=request.user.activeQuestion).questionNumber
                        context["button"] = "Next question"
                        print(context["button"])
                    elif currentQuestion.questionNumber == Quiz.objects.get(id=request.user.activeQuiz).nrOfQuestions - 1:
                        request.user.activeQuestion = Question.objects.get(quiz=Quiz.objects.get(id=request.user.activeQuiz), questionNumber=int(currentQuestion.questionNumber) + 1).id
                        request.user.save()
                        context["questionNo"] = Question.objects.get(id=request.user.activeQuestion).questionNumber
                        context["button"] = "Finish quiz"
                        print(context["button"])
                    else:
                        request.user.finishedQuizzes += (str(quiz.id) + ";")
                        request.user.save()
                        if quiz.showGrade:
                            context["grade"] = 0
                            submissions = Submits.objects.filter(student=request.user.username, quiz_id=quiz.id)
                            for entry in submissions:
                                context["grade"] += entry.points
                        else:
                            context["grade"] = "not_allowed"
                        return render(request, 'finish.html', context)

                    context["question"] = Question.objects.get(id=request.user.activeQuestion).text
                    context["answer"] = Question.objects.get(id=request.user.activeQuestion).answers.split(';')


        else:
            return redirect('error', error_id='no_active_quiz')

        return render(request, 'activeQuiz.html', context)
    else:
        return redirect('error', error_id='no_login')


def completedQuizzes(request):
    if request.user.is_authenticated:
        context = {"quizzes": []}
        finishedQuizzes = request.user.finishedQuizzes.split(';')
        finishedQuizzes.pop()
        print(finishedQuizzes)
        for quiz_id in finishedQuizzes:
            context["quizzes"].append(Quiz.objects.get(id=quiz_id).title + "; " + Quiz.objects.get(id=quiz_id).subject)
            context["grade"] = 0
            submissions = Submits.objects.filter(student=request.user.username, quiz_id=quiz_id)
            for entry in submissions:
                context["grade"] += entry.points
        return render(request, 'completedQuizzes.html', context)
    else:
        return redirect('error', error_id='no_login')

def s_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='no_login')
