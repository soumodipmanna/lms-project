from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from lms_app.models import Student

DEMO_USERS = [
    {
        "username": "alice",
        "email": "alice@example.com",
        "password": "Student@123",
        "name": "Alice",
        "roll_no": "DEMO001",
        "branch": "Computer Science",
    },
    {
        "username": "bob",
        "email": "bob@example.com",
        "password": "Student@123",
        "name": "Bob",
        "roll_no": "DEMO002",
        "branch": "Electrical Engineering",
    },
    {
        "username": "carol",
        "email": "carol@example.com",
        "password": "Student@123",
        "name": "Carol",
        "roll_no": "DEMO003",
        "branch": "Mechanical Engineering",
    },
]


class Command(BaseCommand):
    help = "Idempotently create demo student accounts (alice/bob/carol, password Student@123)."

    def handle(self, *args, **options):
        created_count = 0
        for data in DEMO_USERS:
            user, user_created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "first_name": data["name"],
                },
            )
            if user_created:
                user.set_password(data["password"])
                user.save()

            _, student_created = Student.objects.get_or_create(
                user=user,
                defaults={
                    "roll_no": data["roll_no"],
                    "branch": data["branch"],
                    "name": data["name"],
                    "status": "approved",
                },
            )

            if user_created or student_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"seed_demo_users: Created student '{data['username']}'."
                ))
            else:
                self.stdout.write(
                    f"seed_demo_users: Student '{data['username']}' already exists; skipping."
                )

        if created_count == 0:
            self.stdout.write("seed_demo_users: All demo users already present; nothing to do.")
