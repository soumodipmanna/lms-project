from django.urls import path
from lms_app import views

urlpatterns = [
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),
    path('manage-profile/', views.manage_profile, name='manage_profile'),
    path('admin/approve/<int:borrow_id>/', views.admin_approve_request, name='admin_approve_request'),
    path('', views.home, name='home'),
]
