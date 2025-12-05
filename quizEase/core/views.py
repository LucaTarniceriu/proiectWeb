from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login
import re

# Create your views here.
def welcome(request):

    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        passwordCheck = request.POST["passwordCheck"]

    context = {}
    context['form'] = SignupForm()
    return render(request, "signup.html", context)

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        if re.search("[a-z]+\.[a-z]+[0-9]{2}@e-uvt\.ro", email):
            return redirect("/student")
        elif re.search("[a-z]+\.[a-z]+@e-uvt\.ro", email):
            return redirect("/profesor")
        else:
            print("email invalid")
    return render(request, "login.html")