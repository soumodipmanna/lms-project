from django.urls import path
from lms_app import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),
    path('manage-profile/', views.manage_profile, name='manage_profile'),
    
    path('admin-portal/login/', views.admin_login_view, name='admin_login'),
    path('admin-portal/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-portal/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    path('admin-portal/students/', views.admin_manage_students_view, name='admin_manage_students'),
    path('admin-portal/students/add/', views.admin_add_student_view, name='admin_add_student'),
    path('admin-portal/students/delete/<int:student_id>/', views.admin_delete_student_view, name='admin_delete_student'),
    
    path('admin-portal/books/', views.admin_manage_books_view, name='admin_manage_books'),
    path('admin-portal/books/add/', views.admin_add_book_view, name='admin_add_book'),
    path('admin-portal/books/edit/<int:book_id>/', views.admin_edit_book_view, name='admin_edit_book'),
    path('admin-portal/books/delete/<int:book_id>/', views.admin_delete_book_view, name='admin_delete_book'),
    
    path('admin-portal/borrow-requests/', views.admin_borrow_requests_view, name='admin_borrow_requests'),
    path('admin-portal/borrow-requests/approve/<int:borrow_id>/', views.admin_approve_borrow_view, name='admin_approve_borrow'),
    path('admin-portal/borrow-requests/reject/<int:borrow_id>/', views.admin_reject_borrow_view, name='admin_reject_borrow'),
    
    path('admin-portal/admins/', views.admin_manage_admins_view, name='admin_manage_admins'),
    path('admin-portal/admins/add/', views.admin_add_admin_view, name='admin_add_admin'),
    path('admin-portal/admins/delete/<int:admin_id>/', views.admin_delete_admin_view, name='admin_delete_admin'),
]
