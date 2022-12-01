from .models import Book, Category, BorrowedHistory, Reservation
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from .serializers import BookSerializers, CategorySerializers, UserSerializer, RegisterSerializer, \
    BorrowedHistorySerializer, ReservationSerializers
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page


# allows users to register.
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


# allows the addition of new categories.
class AddCategory(CreateAPIView):
    model = Category
    serializer_class = CategorySerializers


# allows the addition of a new book
class AddBook(CreateAPIView):
    model = Book
    serializer_class = BookSerializers


# used when a book is borrowed.
class AddBorrowedHistory(CreateAPIView):
    model = BorrowedHistory
    serializer_class = BorrowedHistorySerializer


# used when a book is reserved
class AddReservation(CreateAPIView):
    model = Reservation
    serializer_class = ReservationSerializers


# allows searching for books by their categories, name and isbn
class SearchForBook(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['categories', 'name', 'isbn']


# filters the books by their categories.
class BookFilterByCategory(ListAPIView):
    serializer_class = BookSerializers
    paginate_by = 100

    def get_queryset(self):
        categories = self.kwargs['categories']
        return Book.objects.filter(categories=categories)


# filters the books by their name.
class BookFilterByName(ListAPIView):
    serializer_class = BookSerializers
    paginate_by = 100

    def get_queryset(self):
        name = self.kwargs['name']
        return Book.objects.filter(name=name)


# filters the books by their isbn,
class BookFilterByIsbn(ListAPIView):
    serializer_class = BookSerializers
    paginate_by = 100

    def get_queryset(self):
        isbn = self.kwargs['isbn']
        return Book.objects.filter(isbn=isbn)


# filters the books by the person lent to.
class BookFilterByPersonLent(ListAPIView):
    serializer_class = BookSerializers
    paginate_by = 100
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list1 = []
        borrowed = BorrowedHistory.objects.filter(person_lent_to=self.request.user, return_date=None).values('id')
        for i in borrowed:
            list1.append(i["id"])
        return Book.objects.filter(id__in=list1)


# filters the books by their return date.
class BookFilterByReturnDate(ListAPIView):
    serializer_class = BorrowedHistorySerializer
    paginate_by = 100

    def get_queryset(self):
        return_date = self.kwargs['return_date']
        return BorrowedHistory.objects.filter(return_date=return_date)


# shows the details of every book based on its id. The data is cached and is stored for 100 seconds.
@api_view(["GET"])
@cache_page(100)
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializers(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
