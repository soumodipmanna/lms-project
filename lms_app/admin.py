from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from .models import Book, Borrow, Student


@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'quantity')
    search_fields = ('title', 'author', 'isbn')


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'status', 'borrow_date', 'return_date', 'action_buttons')

    def action_buttons(self, obj):
        if obj.status.lower() == 'pending':
            return format_html(
                '<a class="button" style="margin-right:5px; background-color:green; color:white; padding:3px 8px; border-radius:4px;" href="approve/{0}">Approve</a>'
                '<a class="button" style="background-color:red; color:white; padding:3px 8px; border-radius:4px;" href="reject/{0}">Reject</a>',
                obj.id
            )
        elif obj.status.lower() == 'approved':
            return format_html('<span style="color:green;">✔ Approved</span>')
        elif obj.status.lower() == 'rejected':
            return format_html('<span style="color:red;">❌ Rejected</span>')
        return ''
    action_buttons.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:borrow_id>/', self.admin_site.admin_view(self.approve_borrow), name='approve-borrow'),
            path('reject/<int:borrow_id>/', self.admin_site.admin_view(self.reject_borrow), name='reject-borrow'),
        ]
        return custom_urls + urls

    def approve_borrow(self, request, borrow_id):
        borrow = Borrow.objects.get(pk=borrow_id)
        if borrow.book.quantity > 0:
            borrow.book.quantity -= 1
            borrow.book.save()
            borrow.status = 'Approved'
            borrow.message = f"Your borrow request for '{borrow.book.title}' has been approved"
            borrow.save()
            self.message_user(request, f"Borrow request for '{borrow.book.title}' approved.")
        else:
            self.message_user(request, f"Cannot approve '{borrow.book.title}' — out of stock.", level='error')
        return redirect(request.META.get('HTTP_REFERER'))

    def reject_borrow(self, request, borrow_id):
        borrow = Borrow.objects.get(pk=borrow_id)
        borrow.status = 'Rejected'
        borrow.message = f"your borrow request for '{borrow.book.title}' has been rejected"
        borrow.save()
        self.message_user(request, f"Borrow request for '{borrow.book.title}' rejected.")
        return redirect(request.META.get('HTTP_REFERER'))

    def mark_as_returned(self, request, queryset):
        for borrow in queryset:
            if not borrow.is_returned:
                borrow.is_returned = True
                borrow.return_date = timezone.now()
                borrow.save()
                book = borrow.book
                if hasattr(book, 'quantity'):
                    book.quantity = (book.quantity or 0) + 1
                elif hasattr(book, 'available_copies'):
                    book.available_copies = (book.available_copies or 0) + 1
                else:
                    book.quantity = getattr(book, 'quantity', 0) + 1
                book.save()
        self.message_user(request, "Selected records marked as returned.")
    mark_as_returned.short_description = "Mark selected borrow records as returned"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'branch')
    search_fields = ('user__username','roll_no')

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('student','book','borrow_date','return_date','returned')
    list_filter = ('returned','borrow_date')
    search_fields = ('student_username','book_title')


