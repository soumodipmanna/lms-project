from datetime import date, timedelta
from django.core.management.base import BaseCommand
from lms_app.models import Borrow
from lms_app.notifications import (
    send_return_reminder,
    send_overdue_admin_alert,
    send_daily_fine_notification,
)


class Command(BaseCommand):
    help = 'Send scheduled email notifications for book returns, reminders, and fines'

    def handle(self, *args, **options):
        today = date.today()
        active_borrows = Borrow.objects.filter(
            status='approved',
            is_returned=False,
            expected_return_date__isnull=False,
        ).select_related('student', 'student__user', 'book')

        reminder_count = 0
        overdue_count = 0
        fine_count = 0

        for borrow in active_borrows:
            days_until_due = (borrow.expected_return_date - today).days

            if days_until_due in (7, 2, 1):
                sent = send_return_reminder(borrow, days_until_due)
                if sent:
                    reminder_count += 1
                    self.stdout.write(
                        f"  Reminder ({days_until_due}d): {borrow.student.roll_no} - {borrow.book.title}"
                    )

            if days_until_due < 0:
                sent = send_overdue_admin_alert(borrow)
                if sent:
                    overdue_count += 1

                sent = send_daily_fine_notification(borrow)
                if sent:
                    fine_count += 1
                    self.stdout.write(
                        f"  Overdue ({abs(days_until_due)}d): {borrow.student.roll_no} - {borrow.book.title}"
                    )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone: {reminder_count} reminder(s), {overdue_count} overdue alert(s), {fine_count} fine notification(s)"
        ))
