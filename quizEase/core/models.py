from django.db import models

# Create your models here.

from django.db import  models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    isProfesor = models.BooleanField(default=False)
    activeQuiz = models.CharField() # id of quiz that is currently editing or answering


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    instructions = models.CharField(max_length=500)
    showGrade = models.CharField(max_length=100, default="show_grade")
    allowReturn = models.CharField(max_length=100, default="allow_return")
    # createdBy = models.CharField(max_length=100) # email of profesor
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    answers = models.CharField(max_length=1000) # String of answers, separated by ";"
    correctAnswer = models.CharField(max_length=100) # Indexes of correct answer
    points = models.IntegerField()
    questionNumber = models.IntegerField()

class Submits(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.CharField(max_length=100) # email of student
    quizId = models.IntegerField() # id of the answered quiz
    answers = models.CharField(max_length=100) # String of answer indexes (ex. a,b;a;c,d; -> question1: a and b; question2: a; question3: c and d)
    grade = models.CharField(max_length=5) # value of final grade
