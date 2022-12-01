from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    reserve_date = models.DateTimeField(null=True, blank=True)
    person_reserved = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person_reserved")


class BorrowedHistory(models.Model):
    # book foreign key is a string because the model is defined under this section.
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    person_lent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person_lent_to")
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)


class Book(models.Model):
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
