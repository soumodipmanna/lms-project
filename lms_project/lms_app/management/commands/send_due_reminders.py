import logging

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone

from lms_app.models import Borrow, Notification
from lms_app.views import create_notification

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create in-app due-date reminders for borrows due within 24 hours (i.e. tomorrow).'

    def handle(self, *args, **options):
        self.stdout.write('Checking for borrows due tomorrow…')
        created = 0
        skipped = 0

        try:
            today = timezone.now().date()
            tomorrow = today + timezone.timedelta(days=1)

            due_tomorrow = (
                Borrow.objects.filter(
                    is_returned=False,
                    status='approved',
                    expected_return_date=tomorrow,
                )
                .select_related('student', 'book')
            )

            cutoff = timezone.now() - timezone.timedelta(hours=24)

            for borrow in due_tomorrow:
                book_title = borrow.book.title
                message = (
                    f"Reminder: '{book_title}' is due tomorrow. "
                    "Return it on time to avoid a fine."
                )

                already_notified = Notification.objects.filter(
                    Q(message__startswith=f"Reminder: '{book_title}' is due tomorrow") |
                    Q(message__startswith=f'Reminder: "{book_title}" is due tomorrow'),
                    student=borrow.student,
                    created_at__gte=cutoff,
                ).exists()

                if already_notified:
                    skipped += 1
                    continue

                create_notification(borrow.student, message, '/my-borrowed-books/')
                created += 1

        except Exception as exc:
            logger.error('send_due_reminders failed: %s', exc, exc_info=True)
            raise CommandError(f'send_due_reminders failed: {exc}') from exc

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Reminders created: {created}, skipped (already sent): {skipped}.'
            )
        )
