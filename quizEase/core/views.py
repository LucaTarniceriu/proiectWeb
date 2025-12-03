from django.shortcuts import render
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login

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
    context = {}
    context['form'] = LoginForm()
    return render(request, "login.html", context)