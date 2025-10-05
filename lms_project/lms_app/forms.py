from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentSignupForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['roll_no', 'branch']

class StudentLoginForm(forms.Form):
    roll_no = forms.CharField(label='Roll Number')
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your phone number'}),
        }
