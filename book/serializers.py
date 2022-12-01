from rest_framework import serializers
from .models import Book, Category, User, BorrowedHistory, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'email already exists'})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'username already exists'})

        return super().validate(args)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializers(serializers.ModelSerializer):
    # allows us to serialize a many-to-many field.
    categories_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
        # does not show this field.
        extra_kwargs = {'categories': {'write_only': True}}

    def get_categories_detail(self, obj):
        return CategorySerializers(obj.categories.all(), many=True).data


class BorrowedHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedHistory
        fields = "__all__"


class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    # raises a validation error if the reservation date is before the return date.
    def validate(self, data):
        borrowed = list(BorrowedHistory.objects.filter(book=data['book']).values_list('return_date', flat=True))

        for i in borrowed:
            if i is not None:
                if data["reserve_date"] < i:
                    raise serializers.ValidationError("date of reservation not possible")
        return data
