from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentSignupForm(forms.ModelForm):
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)
    email= forms.EmailField()

    class Meta:
        model=Student
        fields=['roll_no','branch']

class StudentLoginForm(forms.Form):
    username= forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)