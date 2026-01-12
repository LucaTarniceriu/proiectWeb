from django.db import models

# Create your models here.

from django.db import  models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    isProfesor = models.BooleanField(default=False) # marcheaza un cont cu permisiuni de profesor
    activeQuiz = models.CharField() # id-ul quiz-ului care este editat sau rezolvat la un moment dat
    activeQuestion = models.CharField() # id-ul intrebarii care este editata sau rezolvata la un moment dat
    finishedQuizzes = models.CharField(blank=True) # o lista de quiz-uri care au fost trimise de un student


class Quiz(models.Model):
    id = models.AutoField(primary_key=True) # id unic al quiz-ului
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    instructions = models.CharField(max_length=500)
    showGrade = models.CharField(max_length=100, default="show_grade") # optiunea care permite afisarea notei imediat dupa trimiterea quiz-ului
    allowReturn = models.CharField(max_length=100, default="allow_return") # optiunea care permite intoarcerea la o intrebare precedenta in timpul rezolvarii quiz-ului
    nrOfQuestions = models.IntegerField() # numarul total al intrebarilor quiz-ului
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE) # obiectul User profesor care a creat quiz-ul


class Question(models.Model):
    id = models.AutoField(primary_key=True) # id unic al intrebarii
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # quiz-ul din care face parte intrebarea
    text = models.CharField(max_length=100) # textul intrebarii
    answers = models.CharField(max_length=1000) # String care contine raspunsurile, separate prin ";"
    correctAnswer = models.CharField(max_length=100) # Indecsi ai raspunsurilor corecte (unul sau mai multe)
    points = models.IntegerField() # punctele corespunzatoare intrebarii
    questionNumber = models.IntegerField() # numarul intrebarii in cadrul quiz-ului

class Submits(models.Model):
    id = models.AutoField(primary_key=True) # id unic al raspunsului la o intrebare
    student = models.CharField(max_length=100) # email studentului care a raspuns la intrebare
    question_id = models.CharField(max_length=100) # id-ul intrebarii la care s-a raspuns
    quiz_id = models.CharField(max_length=100) # id-ul quizului din care face parte intrebarea
    answers = models.CharField(max_length=1000) # String care contine raspunsurile, separate prin ";"
    points = models.IntegerField() # numarul de puncte acordate, in functie de raspuns
