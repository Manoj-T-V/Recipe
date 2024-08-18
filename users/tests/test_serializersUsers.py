import pytest
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Profile
from users.serializers import (
    CustomUserSerializer,
    UserRegisterationSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    ProfileAvatarSerializer,
    PasswordChangeSerializer
)

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(self.user)
        data = serializer.data
        assert data['id'] == self.user.id
        assert data['username'] == self.user.username
        assert data['email'] == self.user.email

@pytest.mark.django_db
class TestUserRegistrationSerializer:
    def test_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        serializer = UserRegisterationSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.check_password('newpassword123')

@pytest.mark.django_db
class TestUserLoginSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')

    def test_valid_login(self):
        data = {'email': 'testuser@example.com', 'password': 'testpass'}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.validate(data)
        assert user == self.user

    def test_invalid_login(self):
        data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
        serializer = UserLoginSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.validate(data)

@pytest.mark.django_db
class TestProfileSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio='This is a bio')

    def test_profile_serializer(self):
        serializer = ProfileSerializer(self.profile)
        data = serializer.data
        assert data['bookmarks'] == []  # Assuming bookmarks is empty by default
        assert data['bio'] == 'This is a bio'

@pytest.mark.django_db
class TestProfileAvatarSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, avatar='avatar/test_image.png')

    def test_profile_avatar_serializer(self):
        serializer = ProfileAvatarSerializer(self.profile)
        data = serializer.data
        assert data['avatar'] == 'avatar/test_image.png'

@pytest.mark.django_db
class TestPasswordChangeSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='oldpassword123')

    def test_valid_password_change(self):
        data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123'
        }
        serializer = PasswordChangeSerializer(data=data, context={'request': type('Request', (object,), {'user': self.user})})
        assert serializer.is_valid()
        serializer.save()
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword123')

    def test_invalid_old_password(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        serializer = PasswordChangeSerializer(data=data, context={'request': type('Request', (object,), {'user': self.user})})
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
