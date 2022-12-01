from celery import shared_task
from .models import Book


# resets the quantity of the books.
@shared_task
def reset_quantity(number_of_books):
    for i in range(1, number_of_books + 1):
        try:
            book = Book.objects.get(id=i)
            book.quantity = 10
            book.save()

        except Book.DoesNotExist:
            pass
