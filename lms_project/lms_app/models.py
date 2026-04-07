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
    department = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
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
    fine_rate = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, help_text='Fine per day in rupees (₹)')

    def __str__(self):
        return self.title

STUDENT_STATUS_CHOICES = (
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('disabled', 'Disabled'),
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=50)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STUDENT_STATUS_CHOICES, default='pending')
    status_reason = models.TextField(blank=True, null=True, help_text='Reason for rejection or disabling')

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
    reject_reason = models.TextField(blank=True, null=True, help_text='Reason for rejection')

    def __str__(self):
        return f"{self.student} - {self.book} ({self.status})"
    
    def calculate_fine(self):
        """Calculate fine if book is overdue, accounting for approved waivers"""
        if self.expected_return_date and not self.is_returned:
            from datetime import date
            today = date.today()
            if today > self.expected_return_date:
                overdue_days = (today - self.expected_return_date).days
                gross_fine = overdue_days * float(self.book.fine_rate)
                total_waived = sum(
                    float(w.waived_amount)
                    for w in self.waivers.filter(status='approved')
                )
                return max(gross_fine - total_waived, 0.0)
        return 0.00


NOTIFICATION_TYPE_CHOICES = (
    ('borrow_confirmed', 'Borrow Confirmed'),
    ('reminder_7day', '7-Day Return Reminder'),
    ('reminder_2day', '2-Day Return Reminder'),
    ('reminder_1day', '1-Day Return Reminder'),
    ('overdue_admin', 'Overdue Alert to Admin'),
    ('fine_daily', 'Daily Fine Notification'),
    ('fine_waived', 'Fine Waived Notification'),
)

class EmailNotificationLog(models.Model):
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    recipient_email = models.EmailField()
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.notification_type} to {self.recipient_email} at {self.sent_at}"


WAIVER_STATUS_CHOICES = (
    ('pending', 'Pending Approval'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

class FineWaiver(models.Model):
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE, related_name='waivers')
    requested_by = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='waiver_requests')
    approved_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='waiver_approvals')
    original_fine = models.DecimalField(max_digits=10, decimal_places=2)
    waived_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=WAIVER_STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Waiver for {self.borrow} - {self.status}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to='social_wall/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} on {self.post.id}: {self.content[:30]}"
