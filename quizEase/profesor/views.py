from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import Quiz, Question, Submits, User

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

        if request.method == "POST":
            quizTitle = request.POST["quiz_title"]
            quizSubject = request.POST["quiz_subject"]
            quizInstructions = request.POST["quiz_instructions"]
            showGrade = request.POST["quiz_show_grade"]
            allowReturn = request.POST.get('quiz_allow_return', "no_return")

            quiz = Quiz.objects.create(title=quizTitle,
                                       subject=quizSubject,
                                       instructions=quizInstructions,
                                       showGrade=showGrade,
                                       allowReturn=allowReturn,
                                       createdBy=request.user,
                                       nrOfQuestions = 0)

            question = Question.objects.create(quiz=quiz,
                                               text=quizTitle,
                                               answers="",
                                               correctAnswer="",
                                               points=0,
                                               questionNumber=0)

            if quiz:
                request.user.activeQuiz = quiz.id
                request.user.save()

                return redirect('addQuestion', questionNumber=1)
            else:
                return redirect('error', error_id='quiz_submission_err')
        return render(request, 'createQuiz.html')
    else:
        return redirect('error', error_id='permission_err')

def addQuestion(request, questionNumber):
    if request.user.is_authenticated and request.user.isProfesor:
        if not request.user.activeQuiz or request.user.activeQuiz == "none":
            return redirect('error', error_id='no_active_quiz')

        if request.method == "POST":
            activeQuiz = Quiz.objects.get(id=request.user.activeQuiz)
            questionText = request.POST["question_text"]
            answers = request.POST["answers"]
            correct_answer = request.POST["correct_answer"]
            points = request.POST["points"]

            answer_list = answers.split(";")
            if len(answer_list[-1]) == 0:
                answer_list.pop()
            correct_answer_index = correct_answer.split(";")
            correct_answer = ""
            if len(correct_answer_index[-1]) == 0:
                correct_answer_index.pop()
            for index in correct_answer_index:
                correct_answer += (answer_list[int(index)]+";")



            question = Question.objects.create(quiz=activeQuiz,
                                       text=questionText,
                                       answers=answers,
                                       correctAnswer=correct_answer,
                                       points=points,
                                       questionNumber=questionNumber)

            if question:
                if request.POST['submit'] == "next":
                    return redirect('addQuestion', questionNumber=questionNumber+1)
                if request.POST['submit'] == "finish":
                    activeQuiz.nrOfQuestions = questionNumber
                    activeQuiz.save()
                    request.user.activeQuiz = "none"
                    return redirect('viewQuizzes')
            else:
                return redirect('error', error_id='quiz_submission_err')
        context = {}
        context['questionNumber'] = questionNumber
        return render(request, "addQuestion.html", context)
    else:
        return redirect('error', error_id='permission_err')

def viewQuizzes(request):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {}
        context['quizDatabase'] = Quiz.objects.filter(createdBy=request.user)
        return render(request, 'viewQuizzes.html', context)
    else:
        return redirect('error', error_id='permission_err')

def solvedQuizzes(request, quiz_id):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {"studentDatabase": []}
        students = User.objects.filter(isProfesor=False)
        for student in students:
            if quiz_id in student.finishedQuizzes.split(';'):
                name = student.username.split("@")[0].split(".")
                context['studentDatabase'].append(name[1].title()[:-2] + " " + name[0].title())
                context["grade"] = 0
                submissions = Submits.objects.filter(student=student.username, quiz_id=quiz_id)
                for entry in submissions:
                    context["grade"] += entry.points
        return render(request, 'solvedQuizzes.html', context)
    else:
        return redirect('error', error_id='permission_err')

def deleteQuiz(request, quiz_id):
    if request.user.is_authenticated and request.user.isProfesor:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
        return redirect('viewQuizzes')
    else:
        return redirect('error', error_id='permission_err')

def p_logout(request):
    if request.user.is_authenticated and request.user.isProfesor:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='permission_err')


