from django.urls import path
from .views import *

urlpatterns = [
    path('book/search/', SearchForBook.as_view()),
    path('book/create/', AddBook.as_view()),
    path('category/create/', AddCategory.as_view()),
    path('book/borrowed-history/', BookFilterByPersonLent.as_view()),
    path('book/add-borrow/', AddBorrowedHistory.as_view()),
    path('book/add-reserve/', AddReservation.as_view()),
    path('book/category/', BookFilterByCategory.as_view()),
    path('book/name/', BookFilterByName.as_view()),
    path('book/isbn/', BookFilterByIsbn.as_view()),
    path('book/return-date/', BookFilterByReturnDate.as_view()),
    path('book/<int:pk>/', book_detail)

]
