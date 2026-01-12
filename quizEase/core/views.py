from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
import re


def welcome(request):
    return render(request, "index.html")

# pagina pentru crearea conturilor de student/profesor
# conturile sunt create si validate be baza email-ului institutional
def signup(request):
    customErrors = []
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        passwordCheck = request.POST["passwordCheck"]

        if passwordCheck == password:
            pass
        else:
            customErrors.append("passwords do not match")

        # la acest moment nu exista un sistem de verificare a detinatorului contului,
        # dar aceasta functionalitate va putea fi implementata prin trimiterea unui cod de verificare
        # adresei de email introduse
        if re.search("[a-z]+\.[a-z]+[0-9]{2}@e-uvt\.ro", email):
            if passwordCheck == password:
                if User.objects.create_user(username=email, email=email, password=password, isProfesor = False):
                    return redirect('login_user')
        elif re.search("[a-z]+\.[a-z]+@e-uvt\.ro", email):
            if passwordCheck == password:
                if User.objects.create_user(username=email, email=email, password=password, isProfesor = True):
                    return redirect('login_user')
        else:
            customErrors.append("provided email not part of institutional group")

    context = {}
    context['form'] = SignupForm()
    context['customErrors'] = customErrors
    return render(request, "signup.html", context)

# autentificarea utilizatorilor
def login_user(request):
    customErrors = []
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        logout(request)
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            # utilizatorul este reidrectionat la pagina de "home" corespunzatoare cu tipul de cont
            if re.search("[a-z]+\.[a-z]+[0-9]{2}@e-uvt\.ro", email):
                return redirect("/student")
            elif re.search("[a-z]+\.[a-z]+@e-uvt\.ro", email):
                return redirect("/profesor")
            else:
                customErrors.append("provided email not part of institutional group")
        else:
            customErrors.append("email or password are incorrect")

    context = {}
    context['form'] = SignupForm()
    context['customErrors'] = customErrors
    return render(request, "login.html", context)

# pagina modulara pentru afisarea erorilor
def error(request, error_id):
    context = {}
    if error_id == "permission_err":
        context['errorMessage'] = "You are not logged in with the right permissions to access this page"
    elif error_id == "no_login":
        context['errorMessage'] = "You are not logged in"
    elif error_id == "quiz_submission_err":
        context['errorMessage'] = "Quiz submission failed"
    elif error_id == "no_active_quiz":
        context['errorMessage'] = "No active quiz"
    elif error_id == "already_responded":
        context['errorMessage'] = "Quiz was already sent"
    else:
        context['errorMessage'] = "Error: something went wrong"

    return render(request, "error.html", context)
