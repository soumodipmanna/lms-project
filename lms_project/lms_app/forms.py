from django import forms
from django.contrib.auth.models import User
from .models import Student, Admin, Book

class StudentSignupForm(forms.ModelForm):
    username = forms.CharField(
        min_length=3,
        max_length=150,
        error_messages={
            'required': 'Username is required.',
            'min_length': 'Username must be at least 3 characters long.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=6,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 6 characters long.',
        }
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )

    class Meta:
        model = Student
        fields = ['roll_no', 'branch']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists. Please choose another.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered. Please use another.')
        return email
    
    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no')
        if not roll_no:
            raise forms.ValidationError('Roll number is required.')
        if Student.objects.filter(roll_no=roll_no).exists():
            raise forms.ValidationError('Roll number already registered.')
        return roll_no

class StudentLoginForm(forms.Form):
    roll_no = forms.CharField(
        label='Roll Number',
        error_messages={
            'required': 'Roll number is required.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Password is required.',
        }
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your phone number'}),
        }

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        error_messages={
            'required': 'Password is required.',
        }
    )

class AdminCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = Admin
        fields = ['name', 'email', 'role']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'quantity', 'category', 'department', 'language', 'fine_rate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter author name'}),
            'isbn': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter ISBN'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter quantity'}),
            'category': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter category'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter department'}),
            'language': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter language'}),
            'fine_rate': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Fine per day (e.g., 5.00)', 'step': '0.01'}),
        }

class StudentCreateForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['roll_no', 'branch', 'name', 'phone_number']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSV File', help_text='Upload a CSV file')

class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'department', 'designation']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter name'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter department'}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter designation'}),
        }

class AdminEditForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'email', 'department', 'designation', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter email'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter department'}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter designation'}),
        }
