# будет в api/serializers.py
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     # validators=[validate_username]
                                     # в ветке feature/user-signup
                                     allow_blank=False)
    email = serializers.EmailField(max_length=254,
                                   # validators=[validate_email]
                                   # в ветке feature/user-signup
                                   allow_blank=False)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class ProfileEditSerializer(CustomUserSerializer):
    role = serializers.CharField(read_only=True)
