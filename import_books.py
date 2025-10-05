import os
import django
import csv

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from lms_app.models import Book

def import_books():
    with open('real_books_500.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Book.objects.create(
                title=row['title'],
                author=row['author'],
                isbn=row['isbn'],
                quantity=int(row['quantity']),
            )

    print("✅ Books imported successfully into PostgreSQL!")

if __name__ == '__main__':
  import_books()

