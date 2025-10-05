from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignupForm, StudentLoginForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Book, Borrow, Student
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from django.contrib import messages


def student_signup(request):
    if request.method == 'POST':
        user_form = StudentSignupForm(request.POST)
        if user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password'],
                email=user_form.cleaned_data['email']
            )
            student = user_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_login')
    else:
        user_form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': user_form})


def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            password = form.cleaned_data['password']
            
            try:
                student = Student.objects.get(roll_no=roll_no)
                user = authenticate(username=student.user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid roll number or password.')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid roll number or password.')
    else:
        form = StudentLoginForm()
    return render(request, 'student_login.html', {'form': form})


def student_logout(request):
    logout(request)
    return redirect('student_login')


@login_required
def dashboard(request):
    books = Book.objects.all()
    return render(request, 'dashboard.html', {'books': books})


@login_required
def borrow_book(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)

        existing_request = Borrow.objects.filter(
            book=book,
            student=request.user.student,
            status__in=['pending', 'approved']
        ).exists()

        if existing_request:
            messages.warning(
                request,
                "You already have a borrow request or have borrowed this book."
            )
        else:
            Borrow.objects.create(
                book=book,
                student=request.user.student,
                status='pending'
            )
            messages.success(
                request,
                "Your borrow request has been sent to the admin."
            )

        return redirect('dashboard')
    else:
        messages.error(request, "You must be logged in to borrow a book.")
        return redirect('student_login')


@login_required
def return_book(request, borrow_id):
    record = get_object_or_404(Borrow, id=borrow_id, student=request.user.student)

    if request.method == 'POST':
        record.is_returned = True
        record.return_date = timezone.now()
        record.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(record).pk,
            object_id=record.id,
            object_repr=force_str(record),
            action_flag=CHANGE,
            change_message=f"Book returned: {record.book.title}"
        )

        return redirect('my_borrowed_books')

    return redirect('my_borrowed_books')


@login_required
def my_borrowed_books(request):
    student = request.user.student
    borrowed = Borrow.objects.filter(student=student).order_by('-borrow_date')
    return render(request, 'my_borrowed_books.html', {'borrowed': borrowed})


@login_required
def manage_profile(request):
    student = request.user.student
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('manage_profile')
    else:
        form = ProfileUpdateForm(instance=student)
    return render(request, 'manage_profile.html', {'form': form, 'student': student})


def home(request):
    return render(request, 'landing.html')


@login_required
def admin_approve_request(request, borrow_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to approve requests.")
        return redirect('dashboard')

    borrow_request = get_object_or_404(Borrow, id=borrow_id)
    book = borrow_request.book
    student = borrow_request.student

    if borrow_request.status != 'approved':
        if book.quantity > 0:
            print("before decreasing quantity:", book.quantity)
            book.quantity -= 1
            book.save()
            print("after decreasing quantity:", book.quantity)

            borrow_request.status = 'approved'
            borrow_request.approve_date = timezone.now()
            borrow_request.save()

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(borrow_request).pk,
                object_id=borrow_request.id,
                object_repr=force_str(borrow_request),
                action_flag=CHANGE,
                change_message=f"Approved borrow request for {borrow_request.book.title}"
            )

            messages.success(request, f"{book.title} borrow request approved for {student.user.username}!")

        else:
            messages.error(request, "Book is out of stock!")
    else:
        messages.info(request, "This request is already approved.")

    return redirect('admin_borrow_requests')


@login_required
def admin_reject_request(request, borrow_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to reject requests.")
        return redirect('dashboard')

    borrow_request = get_object_or_404(Borrow, id=borrow_id)
    student = borrow_request.student

    if borrow_request.status != 'rejected':
        borrow_request.status = 'rejected'
        borrow_request.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(borrow_request).pk,
            object_id=borrow_request.id,
            object_repr=force_str(borrow_request),
            action_flag=CHANGE,
            change_message=f"Rejected borrow request for {borrow_request.book.title}"
        )

        messages.warning(request, f"Your borrow request for {borrow_request.book.title} has been rejected.")

    else:
        messages.info(request, "This request has already been rejected.")

    return redirect('admin_borrow_requests')
