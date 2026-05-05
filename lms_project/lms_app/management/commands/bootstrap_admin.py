import os

from django.core.management.base import BaseCommand

from lms_app.models import Admin


class Command(BaseCommand):
    help = (
        "Idempotently create an initial superadmin from INITIAL_ADMIN_EMAIL "
        "and INITIAL_ADMIN_PASSWORD environment variables. Safe to run on "
        "every container start."
    )

    def handle(self, *args, **options):
        email = os.environ.get('INITIAL_ADMIN_EMAIL', '').strip()
        password = os.environ.get('INITIAL_ADMIN_PASSWORD', '')
        name = os.environ.get('INITIAL_ADMIN_NAME', 'Initial Admin').strip() or 'Initial Admin'

        if not email or not password:
            self.stdout.write(
                "bootstrap_admin: INITIAL_ADMIN_EMAIL or INITIAL_ADMIN_PASSWORD "
                "not set; skipping initial admin creation."
            )
            return

        if Admin.objects.filter(email__iexact=email).exists():
            self.stdout.write(
                f"bootstrap_admin: Admin with email '{email}' already exists; "
                "leaving existing record (and password) untouched."
            )
            return

        admin = Admin(
            email=email,
            name=name,
            role='superadmin',
            is_active=True,
        )
        admin.set_password(password)
        admin.save()

        self.stdout.write(self.style.SUCCESS(
            f"bootstrap_admin: Created initial superadmin '{email}'."
        ))
