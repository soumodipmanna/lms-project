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
    
    path('admin-portal/signup-requests/', views.admin_signup_requests, name='admin_signup_requests'),
    path('admin-portal/signup-requests/approve/<int:student_id>/', views.admin_approve_student, name='admin_approve_student'),
    path('admin-portal/signup-requests/reject/<int:student_id>/', views.admin_reject_student, name='admin_reject_student'),
    
    path('admin-portal/students/', views.admin_manage_students_view, name='admin_manage_students'),
    path('admin-portal/students/add/', views.admin_add_student_view, name='admin_add_student'),
    path('admin-portal/students/import/', views.admin_import_students_view, name='admin_import_students'),
    path('admin-portal/students/sample-csv/', views.download_sample_students_csv, name='download_sample_students_csv'),
    path('admin-portal/students/delete/<int:student_id>/', views.admin_delete_student_view, name='admin_delete_student'),
    path('admin-portal/students/disable/<int:student_id>/', views.admin_disable_student, name='admin_disable_student'),
    
    path('admin-portal/books/', views.admin_manage_books_view, name='admin_manage_books'),
    path('admin-portal/books/add/', views.admin_add_book_view, name='admin_add_book'),
    path('admin-portal/books/import/', views.admin_import_books_view, name='admin_import_books'),
    path('admin-portal/books/sample-csv/', views.download_sample_books_csv, name='download_sample_books_csv'),
    path('admin-portal/books/edit/<int:book_id>/', views.admin_edit_book_view, name='admin_edit_book'),
    path('admin-portal/books/delete/<int:book_id>/', views.admin_delete_book_view, name='admin_delete_book'),
    
    path('admin-portal/borrow-requests/', views.admin_borrow_requests_view, name='admin_borrow_requests'),
    path('admin-portal/borrow-requests/approve/<int:borrow_id>/', views.admin_approve_borrow_view, name='admin_approve_borrow'),
    path('admin-portal/borrow-requests/reject/<int:borrow_id>/', views.admin_reject_borrow_view, name='admin_reject_borrow'),
    path('admin-portal/borrow-requests/return/<int:borrow_id>/', views.admin_return_book_view, name='admin_return_book'),
    
    path('admin-portal/admins/', views.admin_manage_admins_view, name='admin_manage_admins'),
    path('admin-portal/admins/add/', views.admin_add_admin_view, name='admin_add_admin'),
    path('admin-portal/admins/edit/<int:admin_id>/', views.admin_edit_admin_view, name='admin_edit_admin'),
    path('admin-portal/admins/delete/<int:admin_id>/', views.admin_delete_admin_view, name='admin_delete_admin'),
    
    path('admin-portal/profile/', views.admin_manage_profile_view, name='admin_manage_profile'),
    
    path('social-wall/', views.social_wall, name='social_wall'),
    path('social-wall/post/', views.create_post, name='create_post'),
    path('social-wall/like/<int:post_id>/', views.like_post, name='like_post'),
    path('social-wall/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('social-wall/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('social-wall/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
