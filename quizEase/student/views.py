from django.shortcuts import render, redirect
from django.contrib.auth import logout
from core.models import Quiz, Question, Submits

# pagina principala pentru utilizator student
def s_home(request):
    if request.user.is_authenticated:
        context = {}
        name = request.user.username.split("@")[0].split(".")
        context['nameStr'] = name[1].title()[:-2] + " " + name[0].title()
        return render(request, 'homeS.html', context)
    else:
        return redirect('error', error_id='no_login')

# pagina pentru participarea la un quiz folosind id-ul sau
# pagina joinQuiz.html contine un formular care transmite id-ul introdus pagini activeQuiz
def joinQuiz(request):
    if request.user.is_authenticated:
        return render(request, 'joinQuiz.html')
    else:
        return redirect('error', error_id='no_login')

# pagina care incarca quiz-ul activ si intrebarile acestuia din baza de date
def activeQuiz(request):
    if request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            print(request.POST['source'])
            if request.POST["source"] == "join":
                # aceasta secventa se executa daca utilizatorul ajunge pe pagina dupa incarcarea id-ului quizului
                formId = request.POST["quiz_code"]
                finishedQuizzes = request.user.finishedQuizzes.split(";")
                # se verifica daca a fost deja trimis un raspuns pentru quizul selectat
                # in caz afirmativ este incarcata o pagina de eroare
                if formId in finishedQuizzes:
                    return redirect('error', error_id='already_responded')

                # daca nu s-a trimis deja un raspuns la quiz-ul selectat, quiz-ul este incarcat ca si quiz activ
                request.user.activeQuiz = formId
                quiz = Quiz.objects.get(id=formId)
                request.user.activeQuestion = Question.objects.get(quiz=quiz, questionNumber=0).id
                request.user.save()
                # se verifica daca quiz-ul selectat permite intoarcerea la intrebari anterioare
                allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                if allowReturn == "allow_return":
                    context["allowReturn"] = True
                else:
                    context["allowReturn"] = False
                # incarcarea informatiilor despre quiz
                context["title"] = quiz.title
                context["instructions"] = quiz.instructions
                context["questionNo"] = 0
                context["isFirstQuestion"] = True
                context["button"] = "Start quiz"
            if request.POST["source"] == "nextQ":
                # aceasta secventa se executa daca utilizatorul ajunge pe pagina prin trecerea la o alta intrebare (urmatoare sau anterioara)
                if request.POST["submit"] == "Previous Question":
                    # cazul in care utilizatorul se intoarce la o intrebare precedenta
                    print("previous")
                    currentQ = Question.objects.get(id=request.user.activeQuestion).questionNumber
                    allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                    if allowReturn == "allow_return":
                        context["allowReturn"] = True
                    else:
                        context["allowReturn"] = False
                    # se abordeaza cazurile pentru intoarcerea la prima intrebare/ intoarcerea la alte intrebari
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
                    # verificarea raspunsului incarcat de student si calcularea punctajului
                    for answer in request.POST.getlist("answers"):
                        studentAnswers += (answer + ";")
                        correctAnswers = Question.objects.get(id=request.user.activeQuestion).correctAnswer
                        score = 0
                        if correctAnswers == studentAnswers:
                            score = Question.objects.get(id=request.user.activeQuestion).points

                    # crearea obiectului pentru raspunsul la intrebare, sau modificarea lui daca a fost deja creat
                    Submits.objects.update_or_create(student=request.user.email, question_id=Question.objects.get(id=request.user.activeQuestion).id, answers=studentAnswers, quiz_id=quiz.id, points=score)

                elif request.POST["submit"] == "Next question" or request.POST["submit"] == "Finish quiz" or request.POST["submit"] == "Start quiz":
                    # cazul in care utilizatorul trece la urmatoarea intrebare, incepe sau finalizeaza quiz-ul
                    print("next")
                    quiz = Quiz.objects.get(id=request.user.activeQuiz)
                    context["title"] = quiz.title
                    context['questionNo'] = Question.objects.get(id=request.user.activeQuestion).questionNumber
                    allowReturn = Quiz.objects.get(id=request.user.activeQuiz).allowReturn
                    # verificarea daca quiz-ul permite intoarcerea la intrebare precedenta
                    if allowReturn == "allow_return":
                        context["allowReturn"] = True
                    else:
                        context["allowReturn"] = False
                    if int(context["questionNo"]) > 0:
                        studentAnswers = ""
                        # verificarea raspunsului incarcat de student si calcularea punctajului
                        for answer in request.POST.getlist("answers"):
                            studentAnswers += (answer + ";")
                            correctAnswers = Question.objects.get(id=request.user.activeQuestion).correctAnswer
                            score = 0
                            if correctAnswers == studentAnswers:
                                score = Question.objects.get(id=request.user.activeQuestion).points

                        Submits.objects.update_or_create(student=request.user.email, question_id=Question.objects.get(id=request.user.activeQuestion).id, answers=studentAnswers, quiz_id=quiz.id, points=score)

                    context["isFirstQuestion"] = False
                    currentQuestion = Question.objects.get(id=request.user.activeQuestion)

                    # se abordeaza cazurile pentru intoarcerea la prima intrebare/ intoarcerea la alte intrebari
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
                        # cazul in care utilizatorul finalizeaza quiz-ul
                        # se adauga id-ul quizului in lista quiz-urilor trimise
                        # aceste quiz-uri nu pot fi accesate din nou
                        request.user.finishedQuizzes += (str(quiz.id) + ";")
                        request.user.save()
                        # daca este permisa afisarea notei, aceasta este calculata si afisata
                        if quiz.showGrade == "show_grade":
                            context["grade"] = 0
                            submissions = Submits.objects.filter(student=request.user.username, quiz_id=quiz.id)
                            for entry in submissions:
                                context["grade"] += entry.points
                        else:
                            context["grade"] = "hide_grade"
                        return render(request, 'finish.html', context)
                    # incarcarea textului intrebarii si a raspunsurilor pentru afisare
                    context["question"] = Question.objects.get(id=request.user.activeQuestion).text
                    context["answer"] = Question.objects.get(id=request.user.activeQuestion).answers.split(';')


        else:
            return redirect('error', error_id='no_active_quiz')

        return render(request, 'activeQuiz.html', context)
    else:
        return redirect('error', error_id='no_login')

# pagina care afiseaza toate quiz-urile completate
def completedQuizzes(request):
    if request.user.is_authenticated:
        context = {"quizzes": {}, "grades":[]}
        # preluarea id-urilor quiz-urilor finalizate
        finishedQuizzes = request.user.finishedQuizzes.split(';')
        finishedQuizzes.pop()
        print(finishedQuizzes)
        # calculul punctajelor pentru fiecare quiz
        for index in range(len(finishedQuizzes)):
            grade = 0
            submissions = Submits.objects.filter(student=request.user.username, quiz_id=finishedQuizzes[index])
            for entry in submissions:
                grade += entry.points
            context["quizzes"][(Quiz.objects.get(id=finishedQuizzes[index]).title + "; " + Quiz.objects.get(id=finishedQuizzes[index]).subject)] = grade

        return render(request, 'completedQuizzes.html', context)
    else:
        return redirect('error', error_id='no_login')

# terminarea sesiunii
def s_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/quizEase')
    else:
        return redirect('error', error_id='no_login')
