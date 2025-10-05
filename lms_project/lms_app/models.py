from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

ROLE_CHOICES = (
    ('officer', 'Admin Officer'),
    ('superadmin', 'Superadmin'),
)

class Admin(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='officer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.get_role_display()}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.IntegerField(default=1)
    category = models.CharField(max_length=100, default='dummy')
    department = models.CharField(max_length=100, default='dummy')
    language = models.CharField(max_length=50, default='English')
    fine_rate = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, help_text='Fine per day in currency')

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.roll_no

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('returned', 'Returned'),
)

class Borrow(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    message = models.CharField(max_length=255, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student} - {self.book} ({self.status})"
    
    def calculate_fine(self):
        """Calculate fine if book is overdue"""
        if self.expected_return_date and not self.is_returned:
            from datetime import date
            today = date.today()
            if today > self.expected_return_date:
                overdue_days = (today - self.expected_return_date).days
                return overdue_days * float(self.book.fine_rate)
        return 0.00
