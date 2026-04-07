import logging
from datetime import date
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Admin, EmailNotificationLog

logger = logging.getLogger(__name__)


def _send_email(subject, template_name, context, recipient_list, notification_type, borrow=None):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    for recipient in recipient_list:
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                html_message=html_message,
                fail_silently=False,
            )
            EmailNotificationLog.objects.create(
                notification_type=notification_type,
                recipient_email=recipient,
                borrow=borrow,
                subject=subject,
                success=True,
            )
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}")
            EmailNotificationLog.objects.create(
                notification_type=notification_type,
                recipient_email=recipient,
                borrow=borrow,
                subject=subject,
                success=False,
            )


def _already_sent_today(notification_type, borrow, recipient_email=None):
    from django.utils import timezone
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    qs = EmailNotificationLog.objects.filter(
        notification_type=notification_type,
        borrow=borrow,
        sent_at__gte=today_start,
        success=True,
    )
    if recipient_email:
        qs = qs.filter(recipient_email=recipient_email)
    return qs.exists()


def send_borrow_confirmation(borrow):
    student_email = borrow.student.user.email
    student_name = borrow.student.name or borrow.student.roll_no
    book_title = borrow.book.title
    expected_return = borrow.expected_return_date

    context = {
        'student_name': student_name,
        'book_title': book_title,
        'book_author': borrow.book.author,
        'borrow_date': borrow.borrow_date,
        'expected_return_date': expected_return,
    }

    _send_email(
        subject=f"Book Borrowed: {book_title}",
        template_name='emails/borrow_confirmation.html',
        context=context,
        recipient_list=[student_email],
        notification_type='borrow_confirmed',
        borrow=borrow,
    )

    admin_emails = list(Admin.objects.filter(is_active=True).values_list('email', flat=True))
    if admin_emails:
        context['is_admin'] = True
        context['student_roll'] = borrow.student.roll_no
        _send_email(
            subject=f"Book Issued: {book_title} to {borrow.student.roll_no}",
            template_name='emails/borrow_confirmation.html',
            context=context,
            recipient_list=admin_emails,
            notification_type='borrow_confirmed',
            borrow=borrow,
        )


def send_return_reminder(borrow, days_remaining):
    if days_remaining == 7:
        notif_type = 'reminder_7day'
    elif days_remaining == 2:
        notif_type = 'reminder_2day'
    elif days_remaining == 1:
        notif_type = 'reminder_1day'
    else:
        return False

    student_email = borrow.student.user.email
    if _already_sent_today(notif_type, borrow, student_email):
        return False

    student_name = borrow.student.name or borrow.student.roll_no
    context = {
        'student_name': student_name,
        'book_title': borrow.book.title,
        'book_author': borrow.book.author,
        'expected_return_date': borrow.expected_return_date,
        'days_remaining': days_remaining,
    }

    _send_email(
        subject=f"Return Reminder: {borrow.book.title} due in {days_remaining} day(s)",
        template_name='emails/return_reminder.html',
        context=context,
        recipient_list=[student_email],
        notification_type=notif_type,
        borrow=borrow,
    )
    return True


def send_overdue_admin_alert(borrow):
    admin_emails = list(Admin.objects.filter(is_active=True).values_list('email', flat=True))
    if not admin_emails:
        return False

    sent_any = False
    for email in admin_emails:
        if _already_sent_today('overdue_admin', borrow, email):
            continue
        sent_any = True

        overdue_days = (date.today() - borrow.expected_return_date).days
        fine = borrow.calculate_fine()
        student_name = borrow.student.name or borrow.student.roll_no
        context = {
            'student_name': student_name,
            'student_roll': borrow.student.roll_no,
            'book_title': borrow.book.title,
            'expected_return_date': borrow.expected_return_date,
            'overdue_days': overdue_days,
            'fine_amount': fine,
            'fine_rate': borrow.book.fine_rate,
        }

        _send_email(
            subject=f"Overdue Book Alert: {borrow.book.title} - {borrow.student.roll_no}",
            template_name='emails/overdue_admin.html',
            context=context,
            recipient_list=[email],
            notification_type='overdue_admin',
            borrow=borrow,
        )
    return sent_any


def send_daily_fine_notification(borrow):
    student_email = borrow.student.user.email
    if _already_sent_today('fine_daily', borrow, student_email):
        return False

    overdue_days = (date.today() - borrow.expected_return_date).days
    fine = borrow.calculate_fine()
    student_name = borrow.student.name or borrow.student.roll_no

    context = {
        'student_name': student_name,
        'book_title': borrow.book.title,
        'book_author': borrow.book.author,
        'expected_return_date': borrow.expected_return_date,
        'overdue_days': overdue_days,
        'fine_amount': fine,
        'fine_rate': borrow.book.fine_rate,
    }

    _send_email(
        subject=f"Overdue Fine Alert: {borrow.book.title} - Current Fine: Rs.{fine:.2f}",
        template_name='emails/fine_daily.html',
        context=context,
        recipient_list=[student_email],
        notification_type='fine_daily',
        borrow=borrow,
    )
    return True


def send_fine_waiver_notification(borrow, waived_amount, original_fine, new_fine):
    student_email = borrow.student.user.email
    student_name = borrow.student.name or borrow.student.roll_no

    context = {
        'student_name': student_name,
        'book_title': borrow.book.title,
        'original_fine': original_fine,
        'waived_amount': waived_amount,
        'new_fine': new_fine,
    }

    _send_email(
        subject=f"Fine Waiver Approved: {borrow.book.title}",
        template_name='emails/fine_waived.html',
        context=context,
        recipient_list=[student_email],
        notification_type='fine_waived',
        borrow=borrow,
    )
