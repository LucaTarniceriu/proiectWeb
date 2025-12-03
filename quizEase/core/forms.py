from django import forms

class SignupForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    passwordCheck = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    email = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())