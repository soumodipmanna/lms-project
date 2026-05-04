from django.core.management.base import BaseCommand
from lms_app.views import send_due_soon_notifications


class Command(BaseCommand):
    help = 'Send in-app due-date reminder notifications for borrows due within 3 days.'

    def handle(self, *args, **options):
        self.stdout.write('Sending due-date reminder notifications…')
        send_due_soon_notifications()
        self.stdout.write(self.style.SUCCESS('Done.'))
