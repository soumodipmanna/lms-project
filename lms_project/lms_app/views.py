from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignupForm, StudentLoginForm, ProfileUpdateForm, AdminLoginForm, AdminCreateForm, BookForm, StudentCreateForm, CSVUploadForm
from django.contrib.auth.models import User
from .models import Book, Borrow, Student, Admin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from django.contrib import messages
from functools import wraps
import csv
import io
from django.http import HttpResponse


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


def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            messages.error(request, 'Please login to access this page.')
            return redirect('admin_login')
        try:
            admin = Admin.objects.get(id=admin_id, is_active=True)
            request.admin = admin
        except Admin.DoesNotExist:
            del request.session['admin_id']
            messages.error(request, 'Session expired. Please login again.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            messages.error(request, 'Please login to access this page.')
            return redirect('admin_login')
        try:
            admin = Admin.objects.get(id=admin_id, is_active=True)
            if admin.role != 'superadmin':
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('admin_dashboard')
            request.admin = admin
        except Admin.DoesNotExist:
            del request.session['admin_id']
            messages.error(request, 'Session expired. Please login again.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login_view(request):
    if request.session.get('admin_id'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                admin = Admin.objects.get(email=email, is_active=True)
                if admin.check_password(password):
                    request.session['admin_id'] = admin.id
                    request.session['admin_name'] = admin.name
                    request.session['admin_role'] = admin.role
                    messages.success(request, f'Welcome back, {admin.name}!')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'form': form})


@admin_login_required
def admin_logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@admin_login_required
def admin_dashboard_view(request):
    total_students = Student.objects.count()
    total_books = Book.objects.count()
    pending_requests = Borrow.objects.filter(status='pending').count()
    total_admins = Admin.objects.count()
    
    context = {
        'admin': request.admin,
        'total_students': total_students,
        'total_books': total_books,
        'pending_requests': pending_requests,
        'total_admins': total_admins,
    }
    return render(request, 'admin_dashboard.html', context)


@admin_login_required
def admin_manage_students_view(request):
    students = Student.objects.all().select_related('user')
    context = {
        'admin': request.admin,
        'students': students,
    }
    return render(request, 'admin_students.html', context)


@admin_login_required
def admin_add_student_view(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            student = form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, f'Student {student.roll_no} added successfully!')
            return redirect('admin_manage_students')
    else:
        form = StudentCreateForm()
    
    context = {
        'admin': request.admin,
        'form': form,
    }
    return render(request, 'admin_add_student.html', context)


@admin_login_required
def admin_delete_student_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        roll_no = student.roll_no
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, f'Student {roll_no} deleted successfully!')
        return redirect('admin_manage_students')
    return redirect('admin_manage_students')


@admin_login_required
def admin_manage_books_view(request):
    books = Book.objects.all()
    context = {
        'admin': request.admin,
        'books': books,
    }
    return render(request, 'admin_books.html', context)


@admin_login_required
def admin_add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('admin_manage_books')
    else:
        form = BookForm()
    
    context = {
        'admin': request.admin,
        'form': form,
    }
    return render(request, 'admin_add_book.html', context)


@admin_login_required
def admin_edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('admin_manage_books')
    else:
        form = BookForm(instance=book)
    
    context = {
        'admin': request.admin,
        'form': form,
        'book': book,
    }
    return render(request, 'admin_edit_book.html', context)


@admin_login_required
def admin_delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('admin_manage_books')
    return redirect('admin_manage_books')


@admin_login_required
def admin_borrow_requests_view(request):
    borrows = Borrow.objects.all().select_related('student', 'student__user', 'book').order_by('-borrow_date')
    context = {
        'admin': request.admin,
        'borrows': borrows,
    }
    return render(request, 'admin_borrow_requests.html', context)


@admin_login_required
def admin_approve_borrow_view(request, borrow_id):
    borrow_request = get_object_or_404(Borrow, id=borrow_id)
    book = borrow_request.book
    
    if request.method == 'POST':
        if borrow_request.status != 'approved':
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                
                borrow_request.status = 'approved'
                borrow_request.is_approved = True
                borrow_request.approve_date = timezone.now()
                borrow_request.save()
                
                messages.success(request, f'Borrow request approved for {borrow_request.student.roll_no}!')
            else:
                messages.error(request, 'Book is out of stock!')
        else:
            messages.info(request, 'This request is already approved.')
    
    return redirect('admin_borrow_requests')


@admin_login_required
def admin_reject_borrow_view(request, borrow_id):
    borrow_request = get_object_or_404(Borrow, id=borrow_id)
    
    if request.method == 'POST':
        if borrow_request.status != 'rejected':
            borrow_request.status = 'rejected'
            borrow_request.save()
            messages.warning(request, f'Borrow request rejected for {borrow_request.student.roll_no}.')
        else:
            messages.info(request, 'This request has already been rejected.')
    
    return redirect('admin_borrow_requests')


@superadmin_required
def admin_manage_admins_view(request):
    admins = Admin.objects.all()
    context = {
        'admin': request.admin,
        'admins': admins,
    }
    return render(request, 'admin_manage_admins.html', context)


@superadmin_required
def admin_add_admin_view(request):
    if request.method == 'POST':
        form = AdminCreateForm(request.POST)
        if form.is_valid():
            new_admin = form.save(commit=False)
            new_admin.set_password(form.cleaned_data['password'])
            new_admin.save()
            messages.success(request, f'Admin {new_admin.name} added successfully!')
            return redirect('admin_manage_admins')
    else:
        form = AdminCreateForm()
    
    context = {
        'admin': request.admin,
        'form': form,
    }
    return render(request, 'admin_add_admin.html', context)


@superadmin_required
def admin_delete_admin_view(request, admin_id):
    admin_to_delete = get_object_or_404(Admin, id=admin_id)
    
    if admin_to_delete.id == request.admin.id:
        messages.error(request, 'You cannot delete yourself!')
        return redirect('admin_manage_admins')
    
    if request.method == 'POST':
        name = admin_to_delete.name
        admin_to_delete.delete()
        messages.success(request, f'Admin {name} deleted successfully!')
        return redirect('admin_manage_admins')
    
    return redirect('admin_manage_admins')


@admin_login_required
def admin_import_students_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('admin_import_students')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                
                for row in reader:
                    try:
                        with transaction.atomic():
                            username = row.get('username', '').strip()
                            password = row.get('password', '').strip()
                            email = row.get('email', '').strip()
                            roll_no = row.get('roll_no', '').strip()
                            branch = row.get('branch', '').strip()
                            name = row.get('name', '').strip()
                            phone_number = row.get('phone_number', '').strip()
                            
                            if not all([username, password, roll_no, branch]):
                                error_count += 1
                                continue
                            
                            if Student.objects.filter(roll_no=roll_no).exists():
                                error_count += 1
                                continue
                            
                            user = User.objects.create_user(
                                username=username,
                                password=password,
                                email=email if email else f'{username}@example.com'
                            )
                            
                            Student.objects.create(
                                user=user,
                                roll_no=roll_no,
                                branch=branch,
                                name=name if name else '',
                                phone_number=phone_number if phone_number else ''
                            )
                            success_count += 1
                    except Exception as e:
                        error_count += 1
                        continue
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} student(s).')
                if error_count > 0:
                    messages.warning(request, f'{error_count} student(s) failed to import (duplicates or invalid data).')
                
                return redirect('admin_manage_students')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('admin_import_students')
    else:
        form = CSVUploadForm()
    
    context = {
        'admin': request.admin,
        'form': form,
    }
    return render(request, 'admin_import_students.html', context)


@admin_login_required
def admin_import_books_view(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect('admin_import_books')
            
            try:
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                success_count = 0
                error_count = 0
                
                for row in reader:
                    try:
                        with transaction.atomic():
                            title = row.get('title', '').strip()
                            author = row.get('author', '').strip()
                            isbn = row.get('isbn', '').strip()
                            quantity = row.get('quantity', '').strip()
                            category = row.get('category', 'dummy').strip()
                            department = row.get('department', 'dummy').strip()
                            language = row.get('language', 'English').strip()
                            fine_rate = row.get('fine_rate', '5.00').strip()
                            
                            if not all([title, author, isbn, quantity]):
                                error_count += 1
                                continue
                            
                            try:
                                quantity = int(quantity)
                                fine_rate = float(fine_rate)
                            except ValueError:
                                error_count += 1
                                continue
                            
                            if Book.objects.filter(isbn=isbn).exists():
                                error_count += 1
                                continue
                            
                            Book.objects.create(
                                title=title,
                                author=author,
                                isbn=isbn,
                                quantity=quantity,
                                category=category,
                                department=department,
                                language=language,
                                fine_rate=fine_rate
                            )
                            success_count += 1
                    except Exception as e:
                        error_count += 1
                        continue
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} book(s).')
                if error_count > 0:
                    messages.warning(request, f'{error_count} book(s) failed to import (duplicates or invalid data).')
                
                return redirect('admin_manage_books')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
                return redirect('admin_import_books')
    else:
        form = CSVUploadForm()
    
    context = {
        'admin': request.admin,
        'form': form,
    }
    return render(request, 'admin_import_books.html', context)


@admin_login_required
def download_sample_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['username', 'password', 'email', 'roll_no', 'branch', 'name', 'phone_number'])
    writer.writerow(['student1', 'password123', 'student1@example.com', 'CS2023001', 'Computer Science', 'John Doe', '1234567890'])
    writer.writerow(['student2', 'password123', 'student2@example.com', 'CS2023002', 'Computer Science', 'Jane Smith', '0987654321'])
    writer.writerow(['student3', 'password123', 'student3@example.com', 'EC2023001', 'Electronics', 'Bob Wilson', '5555555555'])
    
    return response


@admin_login_required
def download_sample_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_books.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['title', 'author', 'isbn', 'quantity', 'category', 'department', 'language', 'fine_rate'])
    writer.writerow(['Introduction to Python', 'Mark Lutz', '978-1449355739', '10', 'Programming', 'Computer Science', 'English', '5.00'])
    writer.writerow(['Clean Code', 'Robert C. Martin', '978-0132350884', '5', 'Software Engineering', 'Computer Science', 'English', '3.00'])
    writer.writerow(['The Pragmatic Programmer', 'Andrew Hunt', '978-0135957059', '8', 'Software Development', 'Computer Science', 'English', '4.00'])
    
    return response
