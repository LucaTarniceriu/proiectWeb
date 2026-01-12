from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import Quiz, Question, Submits, User

# pagina principala pentru utilizator profesor
def p_home(request):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {}
        name = request.user.username.split("@")[0].split(".")
        context['nameStr'] = name[1].title() + " " + name[0].title()
        return render(request, 'homeP.html', context)
    else:
        return redirect('error', error_id='permission_err')

# pagina pentru crerea unui quiz, cu date precum titlu, subiect, instructiuni etc.
def createQuiz(request):
    if request.user.is_authenticated and request.user.isProfesor:

        if request.method == "POST":
            # Extragere informatii generale quiz din formular
            quizTitle = request.POST["quiz_title"]
            quizSubject = request.POST["quiz_subject"]
            quizInstructions = request.POST["quiz_instructions"]
            showGrade = request.POST["quiz_show_grade"]
            allowReturn = request.POST.get('quiz_allow_return', "no_return")
            # creare obiect quiz in baza de date
            quiz = Quiz.objects.create(title=quizTitle,
                                       subject=quizSubject,
                                       instructions=quizInstructions,
                                       showGrade=showGrade,
                                       allowReturn=allowReturn,
                                       createdBy=request.user,
                                       nrOfQuestions = 0)
            # crearea unei intrebari fara date care marcheaza inceputul quizului
            question = Question.objects.create(quiz=quiz,
                                               text=quizTitle,
                                               answers="",
                                               correctAnswer="",
                                               points=0,
                                               questionNumber=0)

            if quiz:
                # setarea quiz-ului curent ca activ
                request.user.activeQuiz = quiz.id
                request.user.save()
                return redirect('addQuestion', questionNumber=1)
            else:
                return redirect('error', error_id='quiz_submission_err')
        return render(request, 'createQuiz.html')
    else:
        return redirect('error', error_id='permission_err')

# pagina prin care se adauga intrebari noi la quiz-ul creat
def addQuestion(request, questionNumber):
    if request.user.is_authenticated and request.user.isProfesor:
        if not request.user.activeQuiz or request.user.activeQuiz == "none":
            # Verifica daca utilizatorul are un quiz activ inainte de a adauga o intrebare
            return redirect('error', error_id='no_active_quiz')

        if request.method == "POST":
            # Se preiau informatiile despre intrebarea introdusa din formular
            activeQuiz = Quiz.objects.get(id=request.user.activeQuiz)
            questionText = request.POST["question_text"]
            answers = request.POST["answers"]
            correct_answer = request.POST["correct_answer"]
            points = request.POST["points"]

            # formatarea raspunsurilor corecte
            answer_list = answers.split(";")
            if len(answer_list[-1]) == 0:
                answer_list.pop()
            correct_answer_index = correct_answer.split(";")
            correct_answer = ""
            if len(correct_answer_index[-1]) == 0:
                correct_answer_index.pop()
            for index in correct_answer_index:
                correct_answer += (answer_list[int(index)]+";")


            # crearea obiectului intrebare in baza de date
            question = Question.objects.create(quiz=activeQuiz,
                                       text=questionText,
                                       answers=answers,
                                       correctAnswer=correct_answer,
                                       points=points,
                                       questionNumber=questionNumber)

            if question:
                if request.POST['submit'] == "next":
                    # se adauga o noua intrebare
                    return redirect('addQuestion', questionNumber=questionNumber+1)
                if request.POST['submit'] == "finish":
                    # se completeaza numarul final de intrebari al quizului si se salveaza quizul
                    activeQuiz.nrOfQuestions = questionNumber
                    activeQuiz.save()
                    # user-ul nu mai are quizul activ
                    request.user.activeQuiz = "none"
                    return redirect('viewQuizzes')
            else:
                return redirect('error', error_id='quiz_submission_err')
        context = {}
        context['questionNumber'] = questionNumber
        return render(request, "addQuestion.html", context)
    else:
        return redirect('error', error_id='permission_err')

# vizualizarea tuturor quiz-urilor create
def viewQuizzes(request):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {}
        # accesarea obiectelor quiz din baza de date, dupa utilizatorul care a creat quiz-ul
        context['quizDatabase'] = Quiz.objects.filter(createdBy=request.user)
        return render(request, 'viewQuizzes.html', context)
    else:
        return redirect('error', error_id='permission_err')

# vizualizarea studentilor care au trimis un anumit quiz
def solvedQuizzes(request, quiz_id):
    if request.user.is_authenticated and request.user.isProfesor:
        context = {"studentDatabase": {}}
        students = User.objects.filter(isProfesor=False)
        for student in students:
            if quiz_id in student.finishedQuizzes.split(';'):
                # selectarea tuturor studentilor care au trimis quiz-ul cu id-ul quizului selectat
                name = student.username.split("@")[0].split(".")
                grade = 0
                submissions = Submits.objects.filter(student=student.username, quiz_id=quiz_id)
                for entry in submissions:
                    # calcularea notei studentului
                    grade += entry.points
                context['studentDatabase'][(name[1].title()[:-2] + " " + name[0].title())] = grade
        return render(request, 'solvedQuizzes.html', context)
    else:
        return redirect('error', error_id='permission_err')

# stergerea unui quiz creat
def deleteQuiz(request, quiz_id):
    if request.user.is_authenticated and request.user.isProfesor:
        # selectarea si stergerea din baza de date, a quiz-ului folosind ID-ul sau
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
        return redirect('viewQuizzes')
    else:
        return redirect('error', error_id='permission_err')

# terminarea sesiunii
def p_logout(request):
    if request.user.is_authenticated and request.user.isProfesor:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='permission_err')