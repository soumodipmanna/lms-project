import csv
from lms_app.models import Book
with open('real_books_500.csv',newline='',encoding='utf-8') as csvfile:
    reader= csv.DictReader(csvfile)
    for row in reader:
        Book.objects.create(
            title=row['title'],
            author=row['author'],
            isbn=row['isbn'],
            quantity=int(row['quantity'])
        )
print("500 real books added")

